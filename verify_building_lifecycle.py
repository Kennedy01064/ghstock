import os
import sys
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Add the project root to sys.path
sys.path.append(os.getcwd())

from backend import models
from backend.services.building_inventory_service import BuildingInventoryService
from backend.services.inventory_service import InventoryService
from backend.domain.errors import DomainConflictError

# Use a test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_building_lifecycle.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_db():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    
    # Create test user
    user = models.User(username="testuser", password_hash="hash", role="superadmin")
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create test buildings
    b1 = models.Building(name="Building A", address="Address 1")
    b2 = models.Building(name="Building B", address="Address 2")
    db.add(b1)
    db.add(b2)
    db.commit()
    db.refresh(b1)
    db.refresh(b2)
    
    # Create test product with central stock
    product = models.Product(sku="PROD-LIFECYCLE-1", name="Lifecycle Test Product", stock_actual=100, reserved_stock=0)
    db.add(product)
    db.commit()
    db.refresh(product)
    
    return db, user, b1, b2, product

def test_building_lifecycle():
    db, user, b1, b2, product = setup_db()
    
    print("\n--- Phase 5: Building Inventory Lifecycle Verification ---")
    
    # 1. Initial Receipt into Building A
    print("1. Receiving 50 units into Building A...")
    BuildingInventoryService.receive_stock(db, b1.id, product.id, 50, user.id, reference_id=1, reference_type='receive')
    
    inv_a = db.query(models.BuildingInventory).filter_by(building_id=b1.id, product_id=product.id).first()
    assert inv_a.quantity == 50
    print(f"   Building A stock: {inv_a.quantity}")
    
    # Check movement
    move = db.query(models.InventoryMovement).filter_by(building_id=b1.id, movement_type='receive').first()
    assert move is not None
    assert move.quantity == 50
    print("   [OK] Movement logged with building_id")

    # 2. Transfer: A -> B
    print("\n2. Transferring 20 units from Building A to Building B...")
    BuildingInventoryService.transfer_stock(db, b1.id, b2.id, product.id, 20, user.id)
    
    db.refresh(inv_a)
    inv_b = db.query(models.BuildingInventory).filter_by(building_id=b2.id, product_id=product.id).first()
    
    assert inv_a.quantity == 30
    assert inv_b.quantity == 20
    print(f"   Building A stock: {inv_a.quantity}")
    print(f"   Building B stock: {inv_b.quantity}")
    
    # Check paired movements
    move_out = db.query(models.InventoryMovement).filter_by(building_id=b1.id, movement_type='transfer_out').first()
    move_in = db.query(models.InventoryMovement).filter_by(building_id=b2.id, movement_type='transfer_in').first()
    assert move_out.quantity == -20
    assert move_in.quantity == 20
    print("   [OK] Paired transfer movements logged")

    # 3. Return to Central: B -> Central
    print("\n3. Returning 10 units from Building B to Central...")
    old_central_stock = product.stock_actual
    BuildingInventoryService.return_stock(db, b2.id, product.id, 10, user.id, reason="Surplus")
    
    db.refresh(inv_b)
    db.refresh(product)
    assert inv_b.quantity == 10
    assert product.stock_actual == old_central_stock + 10
    print(f"   Building B stock: {inv_b.quantity}")
    print(f"   Central stock updated: {old_central_stock} -> {product.stock_actual}")
    
    # Check movements
    move_ret_out = db.query(models.InventoryMovement).filter_by(building_id=b2.id, movement_type='return_out').first()
    move_ret_in = db.query(models.InventoryMovement).filter_by(building_id=None, movement_type='return_in').first()
    assert move_ret_out.quantity == -10
    assert move_ret_in.quantity == 10
    print("   [OK] Return movements logged (Building -> Central)")

    # 4. Shrinkage: A
    print("\n4. Registering 5 units of shrinkage in Building A...")
    BuildingInventoryService.register_shrinkage(db, b1.id, product.id, 5, user.id, reason="Accidental spill")
    
    db.refresh(inv_a)
    assert inv_a.quantity == 25
    print(f"   Building A stock: {inv_a.quantity}")
    
    move_shrunk = db.query(models.InventoryMovement).filter_by(building_id=b1.id, movement_type='shrinkage').first()
    assert move_shrunk.quantity == -5
    assert move_shrunk.reference_type == "Accidental spill"
    print(f"   [OK] Shrinkage logged with reason: {move_shrunk.reference_type}")

    # 5. Insufficient Stock Validation
    print("\n5. Testing insufficient stock for transfer...")
    try:
        BuildingInventoryService.transfer_stock(db, b1.id, b2.id, product.id, 100, user.id)
        assert False, "Should have raised DomainConflictError"
    except DomainConflictError as e:
        print(f"   [OK] Caught expected error: {e}")

    # 6. History Query
    print("\n6. Testing history query...")
    history_a = BuildingInventoryService.get_history(db, building_id=b1.id)
    assert len(history_a) == 3 # receive, transfer_out, shrinkage
    print(f"   Building A history count: {len(history_a)}")
    
    history_central = BuildingInventoryService.get_history(db, building_id=None)
    assert len(history_central) >= 1
    print(f"   Central history count: {len(history_central)}")

    print("\n--- ALL VERIFICATIONS PASSED ---")
    db.close()

if __name__ == "__main__":
    try:
        test_building_lifecycle()
    finally:
        if os.path.exists("./test_building_lifecycle.db"):
            os.remove("./test_building_lifecycle.db")
