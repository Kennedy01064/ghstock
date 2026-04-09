import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.db.session import SessionLocal
from backend.models import Building, User, Product

def seed():
    db = SessionLocal()
    
    # Check if we already have a user
    if not db.query(User).filter_by(username="testadmin").first():
        u = User(username="testadmin", name="Test Admin", password_hash="hash", role="admin")
        db.add(u)
        
    if not db.query(Building).filter_by(name="Test Building").first():
        b = Building(name="Test Building", address="123 Test St")
        db.add(b)
        
    if not db.query(Product).filter_by(sku="TEST-01").first():
        p = Product(sku="TEST-01", name="Test Product", unit="UN", precio=10.0, stock_actual=10)
        db.add(p)
        
    db.commit()
    print("Seed complete")

if __name__ == "__main__":
    seed()
