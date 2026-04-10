from sqlalchemy.orm import Session, joinedload, selectinload
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError
from backend import models, schemas
from backend.domain.constants import OrderStatus
from backend.services.building_inventory_service import BuildingInventoryService
from backend.domain.errors import (
    ResourceNotFoundError,
    DomainConflictError,
    UnauthorizedError,
    DomainValidationError
)

class OrderService:
    def __init__(self, db: Session, current_user: models.User):
        self.db = db
        self.current_user = current_user

    def _commit_or_conflict(self, error_msg="Data integrity or concurrency violation."):
        try:
            self.db.commit()
        except StaleDataError:
            self.db.rollback()
            raise DomainConflictError("Concurrent update detected. Please try again.")
        except IntegrityError:
            self.db.rollback()
            raise DomainConflictError(error_msg)

    def _assert_order_ownership(self, order: models.Order):
        if self.current_user.role in ("superadmin", "manager"):
            return
        my_building_ids = {b.id for b in self.current_user.assigned_buildings}
        if order.building_id not in my_building_ids:
            raise UnauthorizedError("Not enough privileges for this order")

    def _transition_to(self, order: models.Order, target_status: str, allowed_from: list[str]) -> bool:
        """
        Safely transition order status. Returns True if transition happened,
        False if it was already in target_status (idempotency).
        Raises DomainConflictError if transition is invalid.
        """
        if order.status == target_status:
            return False
            
        if order.status not in allowed_from:
            raise DomainConflictError(
                f"Cannot transition order from {order.status} to {target_status}. "
                f"Expected one of: {', '.join(allowed_from)}"
            )
            
        order.status = target_status
        return True

    def get_order(self, order_id: int) -> models.Order:
        order = self.db.query(models.Order).filter(models.Order.id == order_id).first()
        if not order:
            raise ResourceNotFoundError("Order not found")
        self._assert_order_ownership(order)
        return order

    def create_order(self, order_in: schemas.order.OrderCreate) -> models.Order:
        if self.current_user.role not in ("superadmin", "manager"):
            building = self.db.query(models.Building).filter(
                models.Building.id == order_in.building_id,
                models.Building.admin_id == self.current_user.id
            ).first()
            if not building:
                raise UnauthorizedError("Not enough privileges for this building")

        existing_draft = self.db.query(models.Order).filter(
            models.Order.building_id == order_in.building_id,
            models.Order.status == OrderStatus.DRAFT
        ).first()
        if existing_draft:
            return existing_draft

        order = models.Order(
            building_id=order_in.building_id,
            created_by_id=self.current_user.id,
            status=OrderStatus.DRAFT
        )
        self.db.add(order)
        self._commit_or_conflict("A draft order already exists for this building")
        self.db.refresh(order)
        return order

    def add_order_item(self, order_id: int, item_in: schemas.order.OrderItemCreate) -> models.OrderItem:
        order = self.get_order(order_id)
        if order.status != OrderStatus.DRAFT:
            raise DomainConflictError("Items can only be added to DRAFT orders")
        
        if item_in.quantity <= 0:
            raise DomainConflictError("Quantity must be greater than 0")

        product = self.db.query(models.Product).filter(models.Product.id == item_in.product_id).first()
        if not product:
            raise ResourceNotFoundError("Product not found")

        # --- CATALOG VALIDATION ---
        # If the building has specialized catalog requirements, check them.
        # Check if building has ANY catalog entries.
        catalog_count = self.db.query(models.BuildingProductCatalog).filter(
            models.BuildingProductCatalog.building_id == order.building_id,
            models.BuildingProductCatalog.is_active == True
        ).count()
        
        if catalog_count > 0:
            # Building has a whitelist catalog. Check if this product is in it.
            in_catalog = self.db.query(models.BuildingProductCatalog).filter(
                models.BuildingProductCatalog.building_id == order.building_id,
                models.BuildingProductCatalog.product_id == item_in.product_id,
                models.BuildingProductCatalog.is_active == True
            ).first()
            if not in_catalog:
                raise UnauthorizedError(
                    f"El producto '{product.name}' no está autorizado para este edificio."
                )

        existing_item = self.db.query(models.OrderItem).filter(
            models.OrderItem.order_id == order_id,
            models.OrderItem.product_id == item_in.product_id
        ).first()

        if existing_item:
            existing_item.quantity += item_in.quantity
            existing_item.precio_unitario = product.precio or 0.0
            existing_item.nombre_producto_snapshot = product.name
            self._commit_or_conflict()
            self.db.refresh(existing_item)
            return existing_item

        new_item = models.OrderItem(
            order_id=order_id,
            product_id=product.id,
            quantity=item_in.quantity,
            nombre_producto_snapshot=product.name,
            precio_unitario=product.precio or 0.0,
        )
        self.db.add(new_item)
        self._commit_or_conflict()
        self.db.refresh(new_item)
        return new_item

    def remove_order_item(self, order_id: int, item_id: int):
        order = self.get_order(order_id)
        if order.status != OrderStatus.DRAFT:
            raise DomainConflictError("Items can only be removed from DRAFT orders")

        item = self.db.query(models.OrderItem).filter(
            models.OrderItem.id == item_id,
            models.OrderItem.order_id == order_id
        ).first()
        if not item:
            raise ResourceNotFoundError("Item not found")

        self.db.delete(item)
        self._commit_or_conflict()

    def update_order_item(self, order_id: int, item_id: int, item_in: schemas.order.OrderItemUpdate) -> models.OrderItem:
        order = self.get_order(order_id)
        if order.status != OrderStatus.DRAFT:
            raise DomainConflictError("Items can only be updated in DRAFT orders")

        item = self.db.query(models.OrderItem).filter(
            models.OrderItem.id == item_id,
            models.OrderItem.order_id == order_id
        ).first()
        if not item:
            raise ResourceNotFoundError("Item not found")

        if item_in.quantity < 1:
            raise DomainConflictError("Quantity must be at least 1")

        item.quantity = item_in.quantity
        self._commit_or_conflict()
        self.db.refresh(item)
        return item

    def submit_order(self, order_id: int) -> models.Order:
        order = self.db.query(models.Order).filter(models.Order.id == order_id).with_for_update().first()
        if not order:
            raise ResourceNotFoundError("Order not found")
        self._assert_order_ownership(order)
        
        # Idempotency: skip if already submitted or advanced
        if not self._transition_to(order, OrderStatus.SUBMITTED, [OrderStatus.DRAFT]):
            return order

        if not order.items:
            raise DomainConflictError("Cannot submit empty order")

        self._commit_or_conflict()
        self.db.refresh(order)
        return order

    def reopen_order(self, order_id: int) -> models.Order:
        order = self.db.query(models.Order).filter(models.Order.id == order_id).with_for_update().first()
        if not order:
            raise ResourceNotFoundError("Order not found")
        self._assert_order_ownership(order)
        
        self._transition_to(order, OrderStatus.DRAFT, [OrderStatus.SUBMITTED])
        
        self._commit_or_conflict()
        self.db.refresh(order)
        return order

    def cancel_order(self, order_id: int) -> models.Order:
        order = self.db.query(models.Order).filter(models.Order.id == order_id).with_for_update().first()
        if not order:
            raise ResourceNotFoundError("Order not found")
        self._assert_order_ownership(order)
        
        # Cancel allowed from DRAFT or SUBMITTED
        self._transition_to(order, OrderStatus.CANCELLED, [OrderStatus.DRAFT, OrderStatus.SUBMITTED])

        self._commit_or_conflict()
        self.db.refresh(order)
        return order

    def approve_order(self, order_id: int) -> models.Order:
        """Manager approves the submitted order."""
        if self.current_user.role not in ("superadmin", "manager"):
            raise UnauthorizedError("Only managers can approve orders")
            
        order = self.db.query(models.Order).filter(models.Order.id == order_id).with_for_update().first()
        if not order:
            raise ResourceNotFoundError("Order not found")
            
        self._transition_to(order, OrderStatus.APPROVED, [OrderStatus.SUBMITTED])
        
        self._commit_or_conflict()
        self.db.refresh(order)
        return order

    def reject_order(self, order_id: int) -> models.Order:
        """Manager rejects the submitted order."""
        if self.current_user.role not in ("superadmin", "manager"):
            raise UnauthorizedError("Only managers can reject orders")
            
        order = self.db.query(models.Order).filter(models.Order.id == order_id).with_for_update().first()
        if not order:
            raise ResourceNotFoundError("Order not found")
            
        self._transition_to(order, OrderStatus.REJECTED, [OrderStatus.SUBMITTED])
        
        self._commit_or_conflict()
        self.db.refresh(order)
        return order

    def receive_order(self, order_id: int) -> models.Order:
        order = self.get_order(order_id)
        
        # Idempotency: if already delivered, return success
        if not self._transition_to(order, OrderStatus.DELIVERED, [OrderStatus.DISPATCHED]):
            return order

        for item in order.items:
            item.fulfilled_quantity = item.quantity
            BuildingInventoryService.receive_stock(
                db=self.db,
                building_id=order.building_id,
                product_id=item.product_id,
                quantity=item.quantity,
                actor_id=self.current_user.id,
                reference_id=order.id,
                reference_type='order_delivery'
            )

        self._commit_or_conflict()
        self.db.refresh(order)
        return order
