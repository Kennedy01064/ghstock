
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime

# Add the project root to sys.path
sys.path.append(os.getcwd())

from backend import models
from backend.api.v1.endpoints.dispatch import export_batch_consolidated, export_batch_buildings
from xml.sax.saxutils import escape as xml_escape
from fastapi import HTTPException

# Mock objects for FastAPI dependencies
class MockUser:
    def __init__(self):
        self.name = "Test User"
        self.username = "testuser"
        self.id = 1

def test_pdf_generation():
    # Setup DB session
    engine = create_engine("sqlite:///./dev_stock.db")
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Check if batch 1 exists
        batch = db.query(models.DispatchBatch).filter(models.DispatchBatch.id == 1).first()
        if not batch:
            print("Batch 1 not found in dev_stock.db")
            return
        
        print(f"Found batch 1 with {len(batch.items)} items and {len(batch.orders)} orders.")
        
        user = MockUser()
        
        print("Testing consolidated PDF generation...")
        try:
            resp = export_batch_consolidated(db=db, id=1, current_user=user)
            print("Consolidated PDF generated successfully (StreamingResponse returned).")
        except Exception as e:
            print(f"FAILED consolidated PDF: {str(e)}")
            import traceback
            traceback.print_exc()

        print("\nTesting per-building PDF generation...")
        try:
            resp = export_batch_buildings(db=db, id=1, current_user=user)
            print("Per-building PDF generated successfully (StreamingResponse returned).")
        except Exception as e:
            print(f"FAILED building PDF: {str(e)}")
            import traceback
            traceback.print_exc()
            
    finally:
        db.close()

if __name__ == "__main__":
    test_pdf_generation()
