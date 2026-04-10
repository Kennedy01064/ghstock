import sys
import os
from pathlib import Path

# Add root to sys.path to allow importing backend module
sys.path.append(str(Path(__file__).parent.parent.parent))

from backend.db.session import SessionLocal
from backend.models import User, Building, Product, Order, OrderItem
from backend.domain.constants import OrderStatus
from backend.core.security import get_password_hash

def seed_data():
    db = SessionLocal()
    try:
        print("Seeding CI test data...")

        # 1. Create Users
        users_data = [
            ("krojas", "Kennedy Rojas", "superadmin", "krojas"),
            ("eguzman", "Eduardo Guzman", "admin", "eguzman"),
            ("mgomez", "Maria Gomez", "manager", "mgomez"),
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
        admin_user = db.query(User).filter(User.username == "krojas").first()
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

        # 4. Create sample submitted orders
        manager_user = db.query(User).filter(User.username == "mgomez").first()
        torre_norte = db.query(Building).filter(Building.name == "Torre Norte").first()
        edificio_central = db.query(Building).filter(Building.name == "Edificio Central").first()
        lejia = db.query(Product).filter(Product.sku == "LIM-001").first()
        escoba = db.query(Product).filter(Product.sku == "LIM-002").first()

        if manager_user and torre_norte and edificio_central and lejia and escoba:
            # Check if orders already exist to avoid duplicates
            if not db.query(Order).filter(Order.building_id == torre_norte.id, Order.status == OrderStatus.SUBMITTED).first():
                order1 = Order(building_id=torre_norte.id, created_by_id=manager_user.id, status=OrderStatus.SUBMITTED)
                db.add(order1)
                db.flush()
                db.add(OrderItem(order_id=order1.id, product_id=lejia.id, quantity=5, precio_unitario=lejia.precio))
                db.add(OrderItem(order_id=order1.id, product_id=escoba.id, quantity=2, precio_unitario=escoba.precio))
                print("  - Created submitted order for Torre Norte")

            if not db.query(Order).filter(Order.building_id == edificio_central.id, Order.status == OrderStatus.SUBMITTED).first():
                order2 = Order(building_id=edificio_central.id, created_by_id=manager_user.id, status=OrderStatus.SUBMITTED)
                db.add(order2)
                db.flush()
                db.add(OrderItem(order_id=order2.id, product_id=lejia.id, quantity=10, precio_unitario=lejia.precio))
                print("  - Created submitted order for Edificio Central")

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
