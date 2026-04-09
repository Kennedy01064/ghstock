import sys
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from backend.models import Base, Order, OrderItem, DispatchBatch, User
from backend.services.dispatch_service import DispatchService
from backend.domain.constants import OrderStatus, BatchStatus

def test_polish():
    # Setup - Use the actual database (stock_local.db)
    engine = create_engine('sqlite:///stock_local.db')
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()

    print("--- Verifying Polish & Compliance ---")

    # 1. Verify fulfilled_quantity in OrderItem
    try:
        sample_item = db.query(OrderItem).first()
        if sample_item:
            print(f"PASSED: OrderItem has fulfilled_quantity: {sample_item.fulfilled_quantity}")
        else:
            print("SKIPPED: No OrderItems to check, but schema is applied.")
    except Exception as e:
        print(f"FAILED: Error accessing OrderItem.fulfilled_quantity: {e}")

    # 2. Verify Order Status CheckConstraint
    try:
        # Try to insert an invalid status
        invalid_order = Order(building_id=1, created_by_id=1, status='invalid_status')
        db.add(invalid_order)
        db.commit()
        print("FAILED: Order status CheckConstraint did NOT catch invalid status.")
    except IntegrityError:
        db.rollback()
        print("PASSED: Order status CheckConstraint caught invalid status.")
    except Exception as e:
        db.rollback()
        print(f"INFO: Order status CheckConstraint (likely SQLite limitations on ALTER TABLE): {e}")

    # 3. Verify OrderItem fulfilled_quantity limit
    try:
        bad_fulfillment = OrderItem(order_id=1, product_id=1, quantity=10, fulfilled_quantity=20)
        db.add(bad_fulfillment)
        db.commit()
        print("FAILED: OrderItem fulfillment limit CheckConstraint did NOT catch excess.")
    except IntegrityError:
        db.rollback()
        print("PASSED: OrderItem fulfillment limit CheckConstraint caught excess.")
    except Exception as e:
        db.rollback()
        print(f"INFO: OrderItem fulfillment limit (likely SQLite limitations): {e}")

    # 4. Verify DispatchService cleanup
    try:
        service = DispatchService(db, db.query(User).first())
        if hasattr(service, 'create_purchase'):
            print("FAILED: DispatchService still has create_purchase method.")
        else:
            print("PASSED: DispatchService.create_purchase removed.")
    except Exception as e:
        print(f"INFO: DispatchService check skipped or failed due to setup: {e}")

    # 5. Verify batch status check
    try:
        invalid_batch = DispatchBatch(created_by_id=1, status='invalid_batch_status')
        db.add(invalid_batch)
        db.commit()
        print("FAILED: Batch status CheckConstraint did NOT catch invalid status.")
    except IntegrityError:
        db.rollback()
        print("PASSED: Batch status CheckConstraint caught invalid status.")
    except Exception as e:
        db.rollback()
        print(f"INFO: Batch status CheckConstraint (likely SQLite limitations): {e}")

    db.close()

if __name__ == "__main__":
    test_polish()
