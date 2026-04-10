from sqlalchemy.orm import Session
from backend import models
from backend.domain.errors import DomainConflictError, DomainValidationError
from typing import Optional
import logging
from backend.services.audit_service import audit_service

logger = logging.getLogger(__name__)

class InventoryService:
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
    def reserve_stock(
        db: Session,
        product_id: int,
        quantity: int,
        actor_id: int,
        reference_id: Optional[int] = None,
        reference_type: Optional[str] = 'batch'
    ):
        """
        Increment reserved_stock. Available stock decreases.
        Available = Total - Reserved.
        We must ensure Total >= Reserved + NewReservation.
        """
        if quantity <= 0:
            raise DomainValidationError(f"Reserve quantity must be positive, got {quantity}")

        product = db.query(models.Product).filter(models.Product.id == product_id).with_for_update().first()
        if not product:
            raise DomainValidationError(f"Product {product_id} not found")

        available = product.stock_actual - product.reserved_stock
        if available < quantity:
            raise DomainConflictError(
                f"Insufficient available stock for product {product.name} (SKU: {product.sku}). "
                f"On-hand: {product.stock_actual}, Reserved: {product.reserved_stock}, "
                f"Available: {available}, Requested: {quantity}"
            )

        product.reserved_stock += quantity
        
        audit_service.log_event(
            operation="RESERVE_STOCK",
            actor_id=actor_id,
            request_id=None,
            payload={
                "product_id": product_id,
                "sku": product.sku,
                "quantity": quantity,
                "reference_id": reference_id
            }
        )
        return product

    @staticmethod
    def release_stock(
        db: Session,
        product_id: int,
        quantity: int,
        actor_id: int,
        reference_id: Optional[int] = None,
        reference_type: Optional[str] = 'batch'
    ):
        """
        Decrement reserved_stock. Available stock increases.
        """
        if quantity <= 0:
            raise DomainValidationError(f"Release quantity must be positive, got {quantity}")

        product = db.query(models.Product).filter(models.Product.id == product_id).with_for_update().first()
        if not product:
            raise DomainValidationError(f"Product {product_id} not found")

        if product.reserved_stock < quantity:
            raise DomainConflictError(
                f"Cannot release {quantity} units for product '{product.name}' (SKU: {product.sku}): "
                f"only {product.reserved_stock} units are reserved. "
                f"This indicates a stock ledger inconsistency that must be resolved explicitly."
            )

        product.reserved_stock -= quantity

        audit_service.log_event(
            operation="RELEASE_STOCK",
            actor_id=actor_id,
            request_id=None,
            payload={
                "product_id": product_id,
                "sku": product.sku,
                "quantity": quantity,
                "reference_id": reference_id
            }
        )
        return product

    @staticmethod
    def confirm_dispatch_stock(
        db: Session,
        product_id: int,
        quantity: int,
        actor_id: int,
        building_id: Optional[int] = None,
        reference_id: Optional[int] = None,
        reference_type: Optional[str] = 'batch',
        request_id: Optional[str] = None
    ):
        """
        Finalize dispatch: reduce stock_actual AND reserved_stock.
        """
        if quantity <= 0:
            raise DomainValidationError(f"Dispatch quantity must be positive, got {quantity}")

        product = db.query(models.Product).filter(models.Product.id == product_id).with_for_update().first()
        if not product:
            raise DomainValidationError(f"Product {product_id} not found")

        if product.stock_actual < quantity:
            raise DomainConflictError(f"Insufficient stock for dispatch: {product.name}")

        # Both stock_actual and reserved_stock must be reduced together.
        # reserved_stock must cover the full dispatch quantity; if it does not,
        # the ledger is inconsistent and the operation must be rejected explicitly.
        if product.reserved_stock < quantity:
            raise DomainConflictError(
                f"Cannot confirm dispatch of {quantity} units for product '{product.name}' (SKU: {product.sku}): "
                f"only {product.reserved_stock} units are reserved. "
                f"Reservation must be established before dispatch is confirmed."
            )

        product.stock_actual -= quantity
        product.reserved_stock -= quantity

        InventoryService._create_movement(
            db, product_id, -quantity, 'dispatch', actor_id, building_id, reference_id, reference_type
        )

        # Audit Logging
        audit_service.log_event(
            operation="CONFIRM_DISPATCH",
            actor_id=actor_id,
            request_id=request_id,
            payload={
                "product_id": product_id,
                "sku": product.sku,
                "quantity": quantity,
                "reference_id": reference_id
            }
        )

        return product

    @staticmethod
    def register_purchase(
        db: Session,
        product_id: int,
        quantity: int,
        actor_id: int,
        building_id: Optional[int] = None,
        reference_id: Optional[int] = None
    ):
        """
        Increment stock_actual (purchase intake).
        """
        if quantity <= 0:
            raise DomainValidationError(f"Purchase quantity must be positive, got {quantity}")

        product = db.query(models.Product).filter(models.Product.id == product_id).with_for_update().first()
        if not product:
            raise DomainValidationError(f"Product {product_id} not found")

        product.stock_actual += quantity
        InventoryService._create_movement(
            db, product_id, quantity, 'purchase', actor_id, building_id, reference_id, 'purchase'
        )
        return product

    @staticmethod
    def adjust_stock(
        db: Session,
        product_id: int,
        new_quantity: int,
        actor_id: int,
        building_id: Optional[int] = None,
        reason: str = "Manual Adjustment",
        request_id: Optional[str] = None
    ):
        """
        Force set stock_actual.
        """
        if new_quantity < 0:
            raise DomainValidationError("Stock cannot be adjusted to negative")

        product = db.query(models.Product).filter(models.Product.id == product_id).with_for_update().first()
        if not product:
            raise DomainValidationError(f"Product {product_id} not found")

        old_quantity = product.stock_actual
        delta = new_quantity - product.stock_actual

        # Reject the adjustment before mutating anything.
        # If new_quantity < reserved_stock the DB CHECK constraint would fail anyway,
        # but we surface the error explicitly here with a clear message.
        if new_quantity < product.reserved_stock:
            raise DomainConflictError(
                f"Cannot adjust stock for product '{product.name}' (SKU: {product.sku}) "
                f"to {new_quantity}: {product.reserved_stock} units are currently reserved. "
                f"Release or cancel the reservations before reducing stock below the reserved level."
            )

        product.stock_actual = new_quantity

        InventoryService._create_movement(
            db, product_id, delta, 'adjust', actor_id, building_id, None, reason[:50]
        )

        # Audit Logging
        audit_service.log_event(
            operation="ADJUST_STOCK",
            actor_id=actor_id,
            request_id=request_id,
            payload={
                "product_id": product_id,
                "sku": product.sku,
                "old_quantity": old_quantity,
                "new_quantity": new_quantity,
                "delta": delta,
                "reason": reason
            }
        )

        return product
