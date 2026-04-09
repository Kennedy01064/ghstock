import sys
import os
from pathlib import Path

# Add root to sys.path to allow importing backend module
sys.path.append(str(Path(__file__).parent.parent.parent))

from backend.db.session import SessionLocal
from backend.models import User, Building, Product
from backend.core.security import get_password_hash

def seed_data():
    db = SessionLocal()
    try:
        print("Seeding CI test data...")

        # 1. Create Users aligned with auth.spec.js
        users_data = [
            ("superboss", "Juan CEO", "superadmin", "password123"), # Alternative
            ("krojas", "Kennedy Rojas", "superadmin", "krojas"),
            ("eguzman", "E Guzman", "admin", "eguzman"),
            ("mgomez", "M Gomez", "manager", "mgomez"),
        ]

        for username, name, role, password in users_data:
            user = db.query(User).filter(User.username == username).first()
            if not user:
                user = User(
                    username=username,
                    name=name,
                    role=role,
                    password_hash=get_password_hash(password)
                )
                db.add(user)
                print(f"  - Created user: {username}")

        db.commit()

        # 2. Create sample buildings
        admin_user = db.query(User).filter(User.username == "eguzman").first()
        buildings_data = [
            ("Torre Norte", "Av. Principal 123", admin_user.id if admin_user else None),
            ("Edificio Central", "Calle Florida 456", admin_user.id if admin_user else None),
        ]

        for name, address, admin_id in buildings_data:
            building = db.query(Building).filter(Building.name == name).first()
            if not building:
                building = Building(name=name, address=address, admin_id=admin_id, departments_count=10)
                db.add(building)
                print(f"  - Created building: {name}")

        db.commit()

        # 3. Create sample products
        products_data = [
            ("LIM-001", "Lejía", "Limpieza", 8.50),
            ("LIM-002", "Escoba", "Limpieza", 15.00),
        ]

        for sku, name, cat, price in products_data:
            product = db.query(Product).filter(Product.sku == sku).first()
            if not product:
                product = Product(
                    sku=sku, name=name, categoria=cat, precio=price, 
                    stock_actual=100, stock_minimo=10, unit="Unidad"
                )
                db.add(product)
                print(f"  - Created product: {sku}")

        db.commit()
        print("CI Seeding complete.")

    except Exception as e:
        print(f"Error seeding data: {e}")
        db.rollback()
        raise e
    finally:
        db.close()

if __name__ == "__main__":
    seed_data()
