import sys
import os

# Add the parent directory to the sys.path so we can import backend modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.db.session import SessionLocal
from backend.models import Building, User, Order, OrderItem, Product, DispatchBatch, DispatchBatchItem
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import StaleDataError

def test_constraints():
    db = SessionLocal()
    
    # Needs a dummy user and building
    test_user = db.query(User).first()
    test_building = db.query(Building).first()
    test_product = db.query(Product).first()

    if not test_user or not test_building or not test_product:
        print("Missing required initial data for test")
        return

    # 1. Test draft uniqueness index
    order1 = Order(building_id=test_building.id, created_by_id=test_user.id, status='draft')
    order2 = Order(building_id=test_building.id, created_by_id=test_user.id, status='draft')
    
    db.add(order1)
    db.commit()

    db.add(order2)
    try:
        db.commit()
        print("FAILED: Order Draft Uniqueness was bypassed!")
    except IntegrityError as e:
        db.rollback()
        print("SUCCESS: Order Draft Uniqueness caught correctly.")
        
    db.delete(order1)
    db.commit()

    # 2. Test negative stock constraint
    test_product.stock_actual = -1
    db.add(test_product)
    try:
        db.commit()
        print("FAILED: Negative stock was bypassed!")
    except IntegrityError as e:
        db.rollback()
        print("SUCCESS: Negative stock constraint caught correctly.")

    # 3. Test optimistic locking (StaleDataError)
    # Simulate another session changing the product stock
    db2 = SessionLocal()
    prod_session1 = db.query(Product).first()
    prod_session2 = db2.query(Product).first()

    prod_session1.stock_actual += 10
    db.commit()

    prod_session2.stock_actual += 20
    try:
        db2.commit()
        print("FAILED: Optimistic locking was bypassed!")
    except StaleDataError as e:
        db2.rollback()
        print("SUCCESS: Optimistic locking (StaleDataError) caught correctly.")
    
if __name__ == "__main__":
    test_constraints()
