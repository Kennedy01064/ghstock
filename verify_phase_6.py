import sys
import os
from sqlalchemy.orm import Session
from datetime import date, datetime

# Add project root to path
sys.path.append(os.getcwd())

from backend.db.session import SessionLocal
from backend import models, schemas
from backend.services.purchase_service import PurchaseService
from backend.services.catalog_import_service import CatalogImportService
from backend.domain.errors import DomainValidationError

def test_atomic_purchase_success():
    db = SessionLocal()
    try:
        # Get a real user and product
        user = db.query(models.User).filter(models.User.role == 'admin').first()
        product = db.query(models.Product).first()
        
        initial_stock = product.stock_actual
        
        purchase_in = schemas.purchase.PurchaseCreate(
            supplier="Test Supplier",
            invoice_number="INV-001",
            purchase_date=date.today(),
            total_amount=150.0,
            items=[
                schemas.purchase.PurchaseItemCreate(
                    product_id=product.id,
                    quantity=10,
                    unit_price=15.0
                )
            ]
        )
        
        purchase = PurchaseService.create_purchase(db, purchase_in, user.id)
        
        db.refresh(product)
        print(f"Purchase Created: ID {purchase.id}")
        print(f"Stock Updated: {initial_stock} -> {product.stock_actual}")
        
        assert product.stock_actual == initial_stock + 10
        assert len(purchase.items) == 1
        
        # Check movement
        movement = db.query(models.InventoryMovement).filter(
            models.InventoryMovement.reference_id == purchase.id,
            models.InventoryMovement.reference_type == 'purchase'
        ).first()
        assert movement is not None
        assert movement.quantity == 10
        
        print("✅ test_atomic_purchase_success passed")
    finally:
        db.close()

def test_atomic_purchase_failure_rollback():
    db = SessionLocal()
    try:
        user = db.query(models.User).filter(models.User.role == 'admin').first()
        product = db.query(models.Product).first()
        initial_stock = product.stock_actual
        
        # Try a purchase with one valid and one invalid product
        purchase_in = schemas.purchase.PurchaseCreate(
            supplier="Failing Supplier",
            purchase_date=date.today(),
            items=[
                schemas.purchase.PurchaseItemCreate(
                    product_id=product.id,
                    quantity=5,
                    unit_price=10.0
                ),
                schemas.purchase.PurchaseItemCreate(
                    product_id=999999, # INVALID
                    quantity=1,
                    unit_price=1.0
                )
            ]
        )
        
        try:
            PurchaseService.create_purchase(db, purchase_in, user.id)
            print("❌ test_atomic_purchase_failure_rollback failed (should have raised error)")
        except DomainValidationError as e:
            print(f"Expected error caught: {str(e)}")
            
            # Verify stock was NOT updated for the first item
            db.refresh(product)
            assert product.stock_actual == initial_stock
            print("Stock remained unchanged as expected.")
            
            # Verify no partial purchase record
            p_count = db.query(models.Purchase).filter(models.Purchase.supplier == "Failing Supplier").count()
            assert p_count == 0
            
            print("✅ test_atomic_purchase_failure_rollback passed")
    finally:
        db.close()

def test_import_matching_sku_priority():
    db = SessionLocal()
    try:
        # Create a product with a specific SKU
        test_sku = "SKU-IMPORT-TEST"
        existing = db.query(models.Product).filter(models.Product.sku == test_sku).first()
        if not existing:
            existing = models.Product(name="Old Name", sku=test_sku, stock_actual=0)
            db.add(existing)
            db.commit()
        
        # Scenario: CSV has same SKU but DIFFERENT Name. 
        # Should be detected as UPDATE (SKU priority).
        rows = [
            {"sku": test_sku, "nombre": "New Name", "precio": "25.0"}
        ]
        
        preview = CatalogImportService.preview_import(db, rows, "test.csv")
        
        assert preview.updated_count == 1
        assert preview.preview_rows[0].action == schemas.catalog_import.ImportAction.UPDATE
        assert preview.preview_rows[0].existing_id == existing.id
        print(f"Match detected by SKU: {preview.preview_rows[0].existing_name} -> {preview.preview_rows[0].name}")
        
        print("✅ test_import_matching_sku_priority passed")
    finally:
        db.close()

if __name__ == "__main__":
    test_atomic_purchase_success()
    test_atomic_purchase_failure_rollback()
    test_import_matching_sku_priority()
