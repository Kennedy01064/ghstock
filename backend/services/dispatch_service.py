from datetime import datetime, timezone
from typing import List
from sqlalchemy.orm import Session, selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError
from backend import models, schemas
from backend.domain.constants import BatchStatus, OrderStatus
from backend.services.inventory_service import InventoryService
from backend.domain.errors import (
    ResourceNotFoundError,
    DomainConflictError,
    UnauthorizedError,
    DomainValidationError
)

class DispatchService:
    def __init__(self, db: Session, current_user: models.User):
        self.db = db
        self.current_user = current_user

        if self.current_user.role not in ("superadmin", "manager"):
            raise UnauthorizedError("Only management can perform dispatch operations")

    def _commit_or_conflict(self, error_msg="Data integrity or concurrency violation."):
        try:
            self.db.commit()
        except StaleDataError:
            self.db.rollback()
            raise DomainConflictError("Concurrent update detected. Please try again.")
        except IntegrityError:
            self.db.rollback()
            raise DomainConflictError(error_msg)

    def _transition_batch_to(self, batch: models.DispatchBatch, target_status: str, allowed_from: list[str]) -> bool:
        """
        Safely transition batch status. Returns True if transition happened,
        False if it was already in target_status (idempotency).
        """
        if batch.status == target_status:
            return False
            
        if batch.status not in allowed_from:
            raise DomainConflictError(
                f"Cannot transition batch from {batch.status} to {target_status}. "
                f"Expected one of: {', '.join(allowed_from)}"
            )
            
        batch.status = target_status
        return True

    def consolidate_orders(self, order_ids: List[int]) -> dict:
        orders = self.db.query(models.Order).filter(
            models.Order.id.in_(order_ids),
            models.Order.status == OrderStatus.SUBMITTED
        ).all()

        if not orders:
            raise DomainConflictError("No valid submitted orders found")

        batch = models.DispatchBatch(created_by_id=self.current_user.id, status=BatchStatus.PENDING)
        self.db.add(batch)
        self.db.flush()

        product_totals = {}
        for order in orders:
            batch.orders.append(order)
            order.status = OrderStatus.PROCESSING
            for item in order.items:
                product_totals[item.product_id] = product_totals.get(item.product_id, 0) + item.quantity

        for product_id, total in product_totals.items():
            # Reserve stock for the batch
            InventoryService.reserve_stock(
                db=self.db,
                product_id=product_id,
                quantity=total,
                actor_id=self.current_user.id,
                reference_id=None, # Will update after batch.id is solid or just use batch.id if flushed
                reference_type='batch_reserve'
            )
            self.db.add(models.DispatchBatchItem(
                batch_id=batch.id,
                product_id=product_id,
                total_quantity=total
            ))

        self._commit_or_conflict("Failed to consolidate orders. Data integrity violation (likely insufficient stock).")
        
        # Update references now that we have batch.id if needed, 
        # but the movements already happen in reserve_stock.
        # We can update the reference_id of the movements created if we want more precision.
        
        self.db.refresh(batch)
        return {"batch_id": batch.id, "orders_count": len(orders)}

    def confirm_dispatch(self, batch_id: int):
        batch = self.db.query(models.DispatchBatch).options(
            selectinload(models.DispatchBatch.items),
            selectinload(models.DispatchBatch.orders),
        ).filter(models.DispatchBatch.id == batch_id).with_for_update().first()
        
        if not batch:
            raise ResourceNotFoundError("Batch not found")

        # Idempotency: skip if already dispatched
        if not self._transition_batch_to(batch, BatchStatus.DISPATCHED, [BatchStatus.PENDING]):
            return

        # Process each item using InventoryService
        for item in batch.items:
            InventoryService.confirm_dispatch_stock(
                db=self.db,
                product_id=item.product_id,
                quantity=item.total_quantity,
                actor_id=self.current_user.id,
                reference_id=batch.id,
                reference_type='batch'
            )

        for order in batch.orders:
            order.status = OrderStatus.DISPATCHED

        self._commit_or_conflict()

    def reject_order(self, batch_id: int, order_id: int, rejection_note: str = ""):
        batch = self.db.query(models.DispatchBatch).filter(models.DispatchBatch.id == batch_id).with_for_update().first()
        if not batch:
            raise ResourceNotFoundError("Batch not found")
        if batch.status != BatchStatus.PENDING:
            raise DomainConflictError("Can only reject orders from pending batches")

        order = self.db.query(models.Order).filter(models.Order.id == order_id).first()
        if not order:
            raise ResourceNotFoundError("Order not found")
        if order not in batch.orders:
            raise DomainConflictError("Order does not belong to this batch")

        # Release stock for the rejected order
        for item in order.items:
            InventoryService.release_stock(
                db=self.db,
                product_id=item.product_id,
                quantity=item.quantity,
                actor_id=self.current_user.id,
                reference_id=batch.id,
                reference_type='batch_reject'
            )

        order.rejection_note = rejection_note or "El manager rechazó este pedido sin especificar motivo."
        order.status = OrderStatus.SUBMITTED
        batch.orders.remove(order)

        self.db.flush()
        for bi in list(batch.items):
            self.db.delete(bi)

        product_totals = {}
        for o in batch.orders:
            for item in o.items:
                product_totals[item.product_id] = product_totals.get(item.product_id, 0) + item.quantity

        for product_id, total in product_totals.items():
            self.db.add(models.DispatchBatchItem(batch_id=batch.id, product_id=product_id, total_quantity=total))

        self._commit_or_conflict()

