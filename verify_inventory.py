from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend import models, schemas
from backend.core.config import settings
from backend.services.inventory_service import InventoryService
from backend.services.building_inventory_service import BuildingInventoryService
from backend.domain.errors import DomainConflictError

# Connect to the app's database
engine = create_engine(settings.SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

def test_inventory_engine():
    print("Testing Inventory Engine...")
    
    # Cleanup existing test product to avoid UNIQUE constraint failure
    user = db.query(models.User).first()
    if not user:
        # Create a dummy user for the test if none exists
        user = models.User(username="test_audit_user", password_hash="dummy", role="admin")
        db.add(user)
        db.commit()
        db.refresh(user)

    existing = db.query(models.Product).filter_by(sku="TEST-INV-001").first()
    if existing:
        db.delete(existing)
        db.commit()

    product = models.Product(
        name="Test Inventory Product",
        sku="TEST-INV-001",
        stock_actual=0,
        reserved_stock=0,
        is_active=True
    )
    db.add(product)
    db.commit()
    # 0. Initial Adjustment
    print("Testing Initial Adjustment...")
    # Signature: adjust_stock(db, product_id, new_quantity, actor_id, reason)
    InventoryService.adjust_stock(db, product.id, 100, user.id, "Initial test stock")
    db.commit()
    db.refresh(product)
    print(f"Product created: {product.name}, Stock: {product.stock_actual}")
    
    # 1. Test Reservation
    print("Testing Reservation...")
    # Signature: reserve_stock(db, product_id, quantity, actor_id, reference_id, reference_type)
    InventoryService.reserve_stock(db, product.id, 20, user.id, 123, 'batch')
    db.commit()
    db.refresh(product)
    print(f"Reserved: {product.reserved_stock}, Available: {product.stock_actual - product.reserved_stock}")
    assert product.reserved_stock == 20
    
    # 2. Test Insufficient Stock for Reservation
    print("Testing Insufficient Stock Exception...")
    try:
        InventoryService.reserve_stock(db, product.id, 90, user.id, 123, 'batch')
        print("FAILED: Should have raised DomainConflictError")
    except DomainConflictError as e:
        print(f"SUCCESS: Caught expected error: {e}")

    # 3. Test Confirm Dispatch
    print("Testing Confirm Dispatch...")
    # Signature: confirm_dispatch_stock(db, product_id, quantity, actor_id, reference_id, reference_type)
    InventoryService.confirm_dispatch_stock(db, product.id, 10, user.id, 123, 'batch')
    db.commit()
    db.refresh(product)
    print(f"After dispatch (10): Stock: {product.stock_actual}, Reserved: {product.reserved_stock}")
    assert product.stock_actual == 90
    assert product.reserved_stock == 10
    
    # 4. Test Audit Log
    print("Checking Inventory Movements Audit Log...")
    movements = db.query(models.InventoryMovement).filter_by(product_id=product.id).all()
    for m in movements:
        print(f" - Movement: Type={m.movement_type}, Qty={m.quantity}, Ref={m.reference_type}")
    assert len(movements) >= 3

    # 5. Test Building Consumption (Strict)
    print("Testing Building Consumption (Strict)...")
    building = db.query(models.Building).first()
    if building:
        # Give initial stock to building
        BuildingInventoryService.receive_stock(db, building.id, product.id, 50, user.id)
        db.commit()
        
        # Consume 30
        BuildingInventoryService.consume_stock(db, building.id, product.id, 30, user.id)
        db.commit()
        
        inv = db.query(models.BuildingInventory).filter_by(building_id=building.id, product_id=product.id).first()
        print(f"Building Inv: {inv.quantity}")
        assert inv.quantity == 20
        
        # Try to consume 30 (more than 20)
        try:
            BuildingInventoryService.consume_stock(db, building.id, product.id, 30, user.id)
            print("FAILED: Should have raised DomainConflictError for building stock")
        except DomainConflictError as e:
            print(f"SUCCESS: Caught expected error: {e}")

    print("\nALL TESTS PASSED!")

    # Cleanup
    db.delete(product)
    db.commit()

if __name__ == "__main__":
    test_inventory_engine()
