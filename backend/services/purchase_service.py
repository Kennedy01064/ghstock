from sqlalchemy.orm import Session
from typing import List, Optional

from backend import models, schemas
from backend.services.inventory_service import InventoryService
from backend.domain.errors import DomainValidationError
from backend.services.audit_service import audit_service


class PurchaseService:
    @staticmethod
    def create_purchase(
        db: Session,
        purchase_in: schemas.purchase.PurchaseCreate,
        actor_id: int,
        request_id: Optional[str] = None
    ) -> models.Purchase:
        """
        Create a purchase and all its items atomically.
        Increments stock_actual for each product.
        """
        # 1. Basic validation of items
        if not purchase_in.items:
            raise DomainValidationError("Purchase must have at least one item.")

        # 2. Start a transaction
        calculated_total = 0.0
        
        # 3. Create the purchase header
        purchase_data = purchase_in.model_dump(exclude={'items'})
        purchase = models.Purchase(
            **purchase_data,
            created_by_id=actor_id
        )
        db.add(purchase)
        try:
            db.flush() # Get purchase.id

            # 4. Process each item
            for item_in in purchase_in.items:
                product = db.query(models.Product).with_for_update().filter(
                    models.Product.id == item_in.product_id
                ).first()
                
                if not product:
                    raise DomainValidationError(f"Product ID {item_in.product_id} not found.")

                # Create PurchaseItem
                purchase_item = models.PurchaseItem(
                    purchase_id=purchase.id,
                    product_id=item_in.product_id,
                    quantity=item_in.quantity,
                    unit_price=item_in.unit_price
                )
                db.add(purchase_item)
                
                # Increment Stock
                product.stock_actual += item_in.quantity
                calculated_total += (item_in.quantity * (item_in.unit_price or 0.0))
                
                # Create Inventory Movement
                InventoryService._create_movement(
                    db=db,
                    product_id=product.id,
                    quantity=item_in.quantity,
                    movement_type='purchase',
                    actor_id=actor_id,
                    reference_id=purchase.id,
                    reference_type='purchase'
                )

            # 5. Optional verification of total amount
            if purchase.total_amount and abs(purchase.total_amount - calculated_total) > 0.01:
                if purchase.total_amount == 0:
                    purchase.total_amount = calculated_total

            db.commit()
            db.refresh(purchase)

            # 6. Audit Logging
            audit_service.log_event(
                operation="CREATE_PURCHASE",
                actor_id=actor_id,
                request_id=request_id,
                payload={
                    "purchase_id": purchase.id,
                    "provider": purchase.provider,
                    "total_amount": purchase.total_amount,
                    "item_count": len(purchase_in.items)
                }
            )

            return purchase
        except Exception:
            db.rollback()
            raise


    @staticmethod
    def get_purchase(db: Session, purchase_id: int) -> Optional[models.Purchase]:
        return db.query(models.Purchase).filter(models.Purchase.id == purchase_id).first()

    @staticmethod
    def list_purchases(
        db: Session, skip: int = 0, limit: int = 100
    ) -> List[models.Purchase]:
        return (
            db.query(models.Purchase)
            .order_by(models.Purchase.created_at.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )
