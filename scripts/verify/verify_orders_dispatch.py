import sys
import os

# Add the project root to sys.path
sys.path.append(os.getcwd())

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend.db.session import Base
from backend import models, schemas
from backend.services.order_service import OrderService
from backend.services.dispatch_service import DispatchService
from backend.services.inventory_service import InventoryService
from backend.domain.constants import OrderStatus, BatchStatus
from backend.domain.errors import DomainConflictError

# SQLite for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_orders.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    # Create test data
    admin_user = models.User(username="admin", role="superadmin", password_hash="path")
    db.add(admin_user)
    
    building = models.Building(name="Building A")
    db.add(building)
    db.flush()
    
    building.admin_id = admin_user.id
    
    p1 = models.Product(name="Product 1", sku="P1", stock_actual=100, reserved_stock=0, precio=10.0)
    p2 = models.Product(name="Product 2", sku="P2", stock_actual=50, reserved_stock=0, precio=20.0)
    db.add_all([p1, p2])
    db.commit()
    return db, admin_user, building, p1, p2

def test_order_lifecycle():
    print("\n--- Testing Order Lifecycle ---")
    db, user, building, p1, p2 = setup_db()
    order_service = OrderService(db, user)
    
    # 1. Create Draft
    order = order_service.create_order(schemas.order.OrderCreate(building_id=building.id))
    db.refresh(order)
    print(f"Created Order #{order.id}, Status: {order.status}")
    assert order.status == OrderStatus.DRAFT
    
    # 2. Add Items
    order_service.add_order_item(order.id, schemas.order.OrderItemCreate(product_id=p1.id, quantity=10))
    print("Added 10 of Product 1")
    
    # 3. Submit
    order_service.submit_order(order.id)
    db.refresh(order)
    print(f"Submitted Order, Status: {order.status}")
    assert order.status == OrderStatus.SUBMITTED
    
    # 4. Idempotency: Submit again
    order_service.submit_order(order.id)
    db.refresh(order)
    print("Submitted again (Idempotent check)")
    assert order.status == OrderStatus.SUBMITTED
    
    # 5. Reopen to Draft
    order_service.reopen_order(order.id)
    db.refresh(order)
    print(f"Reopened to {order.status}")
    assert order.status == OrderStatus.DRAFT
    
    # 6. Cancel
    order_service.cancel_order(order.id)
    db.refresh(order)
    print(f"Cancelled Order, Status: {order.status}")
    assert order.status == OrderStatus.CANCELLED
    
    # 7. Try to submit cancelled (Should fail)
    try:
        order_service.submit_order(order.id)
    except DomainConflictError as e:
        print(f"Correctly caught error: {e}")
    
    db.close()

def test_dispatch_workflow():
    print("\n--- Testing Dispatch Workflow ---")
    db, user, building, p1, p2 = setup_db()
    order_service = OrderService(db, user)
    dispatch_service = DispatchService(db, user)
    
    # Setup Order
    order = order_service.create_order(schemas.order.OrderCreate(building_id=building.id))
    order_service.add_order_item(order.id, schemas.order.OrderItemCreate(product_id=p1.id, quantity=10))
    order_service.submit_order(order.id)
    
    # 1. Consolidate
    result = dispatch_service.consolidate_orders([order.id])
    batch_id = result["batch_id"]
    batch = db.query(models.DispatchBatch).filter(models.DispatchBatch.id == batch_id).first()
    db.refresh(order)
    print(f"Consolidated into Batch #{batch_id}, Batch Status: {batch.status}, Order Status: {order.status}")
    assert batch.status == BatchStatus.PENDING
    assert order.status == OrderStatus.PROCESSING
    
    # Check reservation
    db.refresh(p1)
    print(f"Product 1 Stock: {p1.stock_actual}, Reserved: {p1.reserved_stock}")
    assert p1.reserved_stock == 10
    
    # 2. Confirm Dispatch
    dispatch_service.confirm_dispatch(batch_id)
    db.refresh(batch)
    db.refresh(order)
    db.refresh(p1)
    print(f"Batch Confirmed. Batch Status: {batch.status}, Order Status: {order.status}")
    print(f"Product 1 After Dispatch: Stock: {p1.stock_actual}, Reserved: {p1.reserved_stock}")
    assert batch.status == BatchStatus.DISPATCHED
    assert order.status == OrderStatus.DISPATCHED
    assert p1.stock_actual == 90
    assert p1.reserved_stock == 0
    
    # 3. Idempotency: Confirm again
    dispatch_service.confirm_dispatch(batch_id)
    print("Confirmed dispatch again (Idempotent check)")
    assert p1.stock_actual == 90 # No double deduction
    
    # 4. Receive Order
    order_service.receive_order(order.id)
    db.refresh(order)
    print(f"Order Received. Order Status: {order.status}")
    assert order.status == OrderStatus.DELIVERED
    
    # Check Building Inventory
    bi = db.query(models.BuildingInventory).filter(
        models.BuildingInventory.building_id == building.id,
        models.BuildingInventory.product_id == p1.id
    ).first()
    print(f"Building Inventory Stock: {bi.quantity}")
    assert bi.quantity == 10
    
    db.close()

def test_rejection_logic():
    print("\n--- Testing Rejection Logic ---")
    db, user, building, p1, p2 = setup_db()
    order_service = OrderService(db, user)
    dispatch_service = DispatchService(db, user)
    
    # Create two orders
    o1 = order_service.create_order(schemas.order.OrderCreate(building_id=building.id))
    order_service.add_order_item(o1.id, schemas.order.OrderItemCreate(product_id=p1.id, quantity=10))
    order_service.submit_order(o1.id)
    
    # Use different buildings for clean test
    b2 = models.Building(name="Building B")
    db.add(b2)
    db.commit()
    o2 = order_service.create_order(schemas.order.OrderCreate(building_id=b2.id))
    order_service.add_order_item(o2.id, schemas.order.OrderItemCreate(product_id=p1.id, quantity=5))
    order_service.submit_order(o2.id)
    
    db.refresh(p1)
    print(f"Initial Product 1 Reserved: {p1.reserved_stock}") 
    assert p1.reserved_stock == 0
    
    # Consolidate
    res = dispatch_service.consolidate_orders([o1.id, o2.id])
    batch_id = res["batch_id"]
    db.refresh(p1)
    print(f"Consolidated. Product 1 Reserved: {p1.reserved_stock}") # 15
    assert p1.reserved_stock == 15
    
    # Reject o1
    dispatch_service.reject_order(batch_id, o1.id, "Need more info")
    db.refresh(o1)
    db.refresh(p1)
    batch = db.query(models.DispatchBatch).filter(models.DispatchBatch.id == batch_id).first()
    print(f"Order 1 Rejected. Status: {o1.status}, Note: {o1.rejection_note}")
    print(f"Product 1 Reserved after rejection: {p1.reserved_stock}") # 5
    assert o1.status == OrderStatus.SUBMITTED
    assert p1.reserved_stock == 5
    assert len(batch.orders) == 1
    
    # Batch items check
    batch_item = db.query(models.DispatchBatchItem).filter(models.DispatchBatchItem.batch_id == batch_id).first()
    print(f"Batch Item Total for P1: {batch_item.total_quantity}")
    assert batch_item.total_quantity == 5
    
    db.close()

if __name__ == "__main__":
    try:
        test_order_lifecycle()
        test_dispatch_workflow()
        test_rejection_logic()
        print("\nALL PHASE 4 TESTS PASSED!")
    finally:
        pass
