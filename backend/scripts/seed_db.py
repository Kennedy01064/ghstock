from app import create_app
from app.extensions import db
from app.models import User, Building, Product, Order, OrderItem, InventoryMovement

app = create_app()

def seed_data():
    with app.app_context():
        db.create_all()

        print("Poblando datos iniciales...")

        # Crear Usuarios si no existen (con contraseñas hasheadas)
        if not User.query.first():
            superadmin = User(username='superboss', name='Juan Pérez (CEO)', role='superadmin')
            superadmin.set_password('password123')

            admin1 = User(username='admin_juan', name='Juan López', role='admin')
            admin1.set_password('password123')

            admin2 = User(username='admin_maria', name='María García', role='admin')
            admin2.set_password('password123')

            manager = User(username='manager_pedro', name='Pedro Gerente', role='manager')
            manager.set_password('password123')

            db.session.add_all([superadmin, admin1, admin2, manager])
            db.session.commit()
            print("Usuarios creados con contraseñas hasheadas.")

        superadmin = User.query.filter_by(username='superboss').first()
        admin_juan = User.query.filter_by(username='admin_juan').first()
        admin_maria = User.query.filter_by(username='admin_maria').first()

        # Crear Edificios si no existen
        if not Building.query.first():
            b1 = Building(name='Torre Norte', address='Av. Principal 123', departments_count=40, admin_id=admin_juan.id if admin_juan else None)
            b2 = Building(name='Edificio Central', address='Calle Florida 456', departments_count=60, admin_id=admin_juan.id if admin_juan else None)
            b3 = Building(name='Complejo Sur', address='Ruta Nacional 789', departments_count=25, admin_id=admin_maria.id if admin_maria else None)
            db.session.add_all([b1, b2, b3])
            db.session.commit()
            print("Edificios creados y asignados.")

        # Crear Productos si no existen
        if not Product.query.first():
            p1 = Product(
                sku='LIM-001', name='Lejía',
                description='Lejía concentrada de 1 litro. Ideal para desinfección de superficies y pisos. Elimina el 99.9% de gérmenes.',
                unit='Litro', precio=8.50,
                imagen_url='https://cdn-icons-png.flaticon.com/512/2674/2674486.png',
                stock_actual=5, stock_minimo=15
            )
            p2 = Product(
                sku='LIM-002', name='Escoba Mágica',
                description='Escoba de cerdas duras con mango ergonómico de aluminio. Perfecta para barrer exteriores y áreas de alto tráfico.',
                unit='Unidad', precio=25.00,
                imagen_url='https://cdn-icons-png.flaticon.com/512/2721/2721990.png',
                stock_actual=30, stock_minimo=10
            )
            p3 = Product(
                sku='LIM-003', name='Papel Toalla',
                description='Paquete de 3 rollos de papel toalla absorbente de doble hoja. Alta resistencia para uso industrial.',
                unit='Paquete', precio=12.90,
                imagen_url='https://cdn-icons-png.flaticon.com/512/2921/2921822.png',
                stock_actual=8, stock_minimo=20
            )
            p4 = Product(
                sku='LIM-004', name='Detergente Multiusos',
                description='Galón de 4 litros de detergente multiusos con aroma a lavanda. Rinde hasta 200 lavadas.',
                unit='Galón', precio=35.00,
                imagen_url='https://cdn-icons-png.flaticon.com/512/2722/2722007.png',
                stock_actual=40, stock_minimo=10
            )
            p5 = Product(
                sku='LIM-005', name='Bolsas de Basura Grandes',
                description='Paquete de 50 bolsas negras extra-resistentes de 75 litros. Material biodegradable.',
                unit='Paquete', precio=18.50,
                imagen_url='https://cdn-icons-png.flaticon.com/512/3063/3063076.png',
                stock_actual=3, stock_minimo=25
            )
            db.session.add_all([p1, p2, p3, p4, p5])
            db.session.commit()

            for p in [p1, p2, p3, p4, p5]:
                mov = InventoryMovement(
                    product_id=p.id, quantity=p.stock_actual,
                    movement_type='in', created_by_id=superadmin.id
                )
                db.session.add(mov)
            db.session.commit()
            print("Productos creados con stock, precios, imágenes y stock mínimo.")

        # Crear Pedidos de prueba
        if not Order.query.first():
            products = Product.query.all()
            buildings = Building.query.all()

            o1 = Order(building_id=buildings[0].id, created_by_id=admin_juan.id, status='submitted')
            db.session.add(o1)
            db.session.commit()
            db.session.add(OrderItem(order_id=o1.id, product_id=products[0].id, quantity=5))
            db.session.add(OrderItem(order_id=o1.id, product_id=products[2].id, quantity=10))

            o2 = Order(building_id=buildings[0].id, created_by_id=admin_juan.id, status='draft')
            db.session.add(o2)
            db.session.commit()
            db.session.add(OrderItem(order_id=o2.id, product_id=products[4].id, quantity=20))

            o3 = Order(building_id=buildings[1].id, created_by_id=admin_juan.id, status='submitted')
            db.session.add(o3)
            db.session.commit()
            db.session.add(OrderItem(order_id=o3.id, product_id=products[0].id, quantity=3))
            db.session.add(OrderItem(order_id=o3.id, product_id=products[3].id, quantity=2))

            o4 = Order(building_id=buildings[1].id, created_by_id=admin_juan.id, status='submitted')
            db.session.add(o4)
            db.session.commit()
            db.session.add(OrderItem(order_id=o4.id, product_id=products[1].id, quantity=4))
            db.session.add(OrderItem(order_id=o4.id, product_id=products[2].id, quantity=6))

            o5 = Order(building_id=buildings[2].id, created_by_id=admin_maria.id, status='submitted')
            db.session.add(o5)
            db.session.commit()
            db.session.add(OrderItem(order_id=o5.id, product_id=products[3].id, quantity=5))
            db.session.add(OrderItem(order_id=o5.id, product_id=products[4].id, quantity=15))

            db.session.commit()
            print("Pedidos de prueba creados.")

        print("\n¡Base de datos poblada exitosamente!")
        print("\n--- CREDENCIALES DE ACCESO ---")
        print("  Superadmin: superboss / password123")
        print("  Admin:      admin_juan / password123")
        print("  Admin:      admin_maria / password123")
        print("------------------------------\n")

if __name__ == '__main__':
    seed_data()
