from sqlalchemy.orm import Session
from backend import models
from backend.domain.errors import DomainConflictError, DomainValidationError
from typing import Optional, List
from datetime import datetime, timezone
import logging

logger = logging.getLogger(__name__)

class BuildingInventoryService:
    @staticmethod
    def _create_movement(
        db: Session,
        product_id: int,
        quantity: int,
        movement_type: str,
        actor_id: int,
        building_id: Optional[int] = None,
        reference_id: Optional[int] = None,
        reference_type: Optional[str] = None
    ):
        """
        Internal helper to create a movement record.
        """
        movement = models.InventoryMovement(
            product_id=product_id,
            quantity=quantity,
            movement_type=movement_type,
            created_by_id=actor_id,
            building_id=building_id,
            reference_id=reference_id,
            reference_type=reference_type
        )
        db.add(movement)
        return movement

    @staticmethod
    def receive_stock(
        db: Session,
        building_id: int,
        product_id: int,
        quantity: int,
        actor_id: int,
        reference_id: Optional[int] = None,
        reference_type: Optional[str] = 'receive'
    ):
        """
        Increment building inventory (after dispatch/transfer).
        """
        if quantity <= 0:
            raise DomainValidationError(f"Receive quantity must be positive, got {quantity}")

        inv = db.query(models.BuildingInventory).filter_by(
            building_id=building_id,
            product_id=product_id
        ).with_for_update().first()

        if not inv:
            inv = models.BuildingInventory(
                building_id=building_id,
                product_id=product_id,
                quantity=0
            )
            db.add(inv)

        inv.quantity += quantity
        BuildingInventoryService._create_movement(
            db, product_id, quantity, 'receive', actor_id, building_id, reference_id, reference_type
        )
        return inv

    @staticmethod
    def consume_stock(
        db: Session,
        building_id: int,
        product_id: int,
        quantity: int,
        actor_id: int,
        reason: Optional[str] = 'consumption'
    ):
        """
        Decrement building inventory for actual usage.
        STRICT: Never clamps. Fails if requested > available.
        """
        if quantity <= 0:
            raise DomainValidationError(f"Consume quantity must be positive, got {quantity}")

        inv = db.query(models.BuildingInventory).filter_by(
            building_id=building_id,
            product_id=product_id
        ).with_for_update().first()

        if not inv or inv.quantity < quantity:
            available = inv.quantity if inv else 0
            raise DomainConflictError(
                f"Insufficient building inventory for consumption. Available: {available}, Requested: {quantity}"
            )

        inv.quantity -= quantity
        
        # Log consumption for usage reporting
        db.add(models.ConsumptionLog(
            building_id=building_id,
            product_id=product_id,
            reported_by_id=actor_id,
            quantity_consumed=quantity
        ))
        
        # Also log as movement for unified audit
        BuildingInventoryService._create_movement(
            db, product_id, -quantity, 'consume', actor_id, building_id, None, reason[:50]
        )
        return inv

    @staticmethod
    def adjust_stock(
        db: Session,
        building_id: int,
        product_id: int,
        new_quantity: int,
        actor_id: int,
        reason: str = "Manual Adjustment"
    ):
        """
        Force set building inventory quantity (Correction).
        """
        if new_quantity < 0:
            raise DomainValidationError("Building stock cannot be adjusted to negative")

        inv = db.query(models.BuildingInventory).filter_by(
            building_id=building_id,
            product_id=product_id
        ).with_for_update().first()

        if not inv:
            inv = models.BuildingInventory(
                building_id=building_id,
                product_id=product_id,
                quantity=0
            )
            db.add(inv)

        delta = new_quantity - inv.quantity
        if delta == 0:
            return inv

        inv.quantity = new_quantity
        
        BuildingInventoryService._create_movement(
            db, product_id, delta, 'adjust', actor_id, building_id, None, reason[:50]
        )
        return inv

    @staticmethod
    def transfer_stock(
        db: Session,
        from_building_id: int,
        to_building_id: int,
        product_id: int,
        quantity: int,
        actor_id: int
    ):
        """
        Move stock from one building to another.
        """
        if quantity <= 0:
            raise DomainValidationError("Transfer quantity must be positive")
        if from_building_id == to_building_id:
            raise DomainValidationError("Source and target buildings must be different")

        # Source building reduction
        source_inv = db.query(models.BuildingInventory).filter_by(
            building_id=from_building_id,
            product_id=product_id
        ).with_for_update().first()

        if not source_inv or source_inv.quantity < quantity:
            available = source_inv.quantity if source_inv else 0
            raise DomainConflictError(f"Insufficient stock in source building. Available: {available}")

        source_inv.quantity -= quantity
        BuildingInventoryService._create_movement(
            db, product_id, -quantity, 'transfer_out', actor_id, from_building_id, to_building_id, 'building'
        )

        # Target building increment
        target_inv = db.query(models.BuildingInventory).filter_by(
            building_id=to_building_id,
            product_id=product_id
        ).with_for_update().first()

        if not target_inv:
            target_inv = models.BuildingInventory(
                building_id=to_building_id,
                product_id=product_id,
                quantity=0
            )
            db.add(target_inv)

        target_inv.quantity += quantity
        BuildingInventoryService._create_movement(
            db, product_id, quantity, 'transfer_in', actor_id, to_building_id, from_building_id, 'building'
        )

        return (source_inv, target_inv)

    @staticmethod
    def return_stock(
        db: Session,
        building_id: int,
        product_id: int,
        quantity: int,
        actor_id: int,
        reason: str = 'Return to Central'
    ):
        """
        Return stock from building back to central warehouse.
        """
        if quantity <= 0:
            raise DomainValidationError("Return quantity must be positive")

        # Building reduction
        inv = db.query(models.BuildingInventory).filter_by(
            building_id=building_id,
            product_id=product_id
        ).with_for_update().first()

        if not inv or inv.quantity < quantity:
            available = inv.quantity if inv else 0
            raise DomainConflictError(f"Insufficient stock in building to return. Available: {available}")

        inv.quantity -= quantity
        BuildingInventoryService._create_movement(
            db, product_id, -quantity, 'return_out', actor_id, building_id, None, reason[:50]
        )

        # Central increment
        product = db.query(models.Product).filter(models.Product.id == product_id).with_for_update().first()
        if not product:
            raise DomainValidationError("Product not found")

        product.stock_actual += quantity
        BuildingInventoryService._create_movement(
            db, product_id, quantity, 'return_in', actor_id, None, building_id, 'building'
        )

        return inv

    @staticmethod
    def register_shrinkage(
        db: Session,
        building_id: int,
        product_id: int,
        quantity: int,
        actor_id: int,
        reason: str
    ):
        """
        Register unrecoverable loss or damage.
        """
        if quantity <= 0:
            raise DomainValidationError("Shrinkage quantity must be positive")
        if not reason:
            raise DomainValidationError("Reason is required for shrinkage")

        inv = db.query(models.BuildingInventory).filter_by(
            building_id=building_id,
            product_id=product_id
        ).with_for_update().first()

        if not inv or inv.quantity < quantity:
            available = inv.quantity if inv else 0
            raise DomainConflictError(f"Insufficient stock for shrinkage. Available: {available}")

        inv.quantity -= quantity
        BuildingInventoryService._create_movement(
            db, product_id, -quantity, 'shrinkage', actor_id, building_id, None, reason[:50]
        )

        return inv

    @staticmethod
    def get_history(
        db: Session,
        building_id: Optional[int] = None,
        product_id: Optional[int] = None,
        movement_type: Optional[str] = None,
        limit: int = 100,
        skip: int = 0
    ) -> List[models.InventoryMovement]:
        """
        Query building/central movement history.
        """
        query = db.query(models.InventoryMovement)
        if building_id is not None:
            query = query.filter(models.InventoryMovement.building_id == building_id)
        if product_id:
            query = query.filter(models.InventoryMovement.product_id == product_id)
        if movement_type:
            query = query.filter(models.InventoryMovement.movement_type == movement_type)
        
        return query.order_by(models.InventoryMovement.created_at.desc()).offset(skip).limit(limit).all()
