from datetime import date, datetime, timedelta, timezone

from sqlalchemy.orm import Session

from backend import models
from backend.core.security import get_password_hash
from backend.db.session import Base, SessionLocal, engine


def bootstrap_database() -> None:
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        if db.query(models.User.id).first():
            _apply_local_fixes(db)
            return
        _seed_initial_data(db)
    finally:
        db.close()


def _apply_local_fixes(db: Session) -> None:
    user = db.query(models.User).filter(models.User.username == "krojas").first()
    if user:
        user.name = "Kennedy Rojas"
        user.role = "superadmin"
    manager = db.query(models.User).filter(models.User.username == "mgomez").first()
    if manager:
        manager.role = "manager"
    if user or manager:
        db.commit()


def _seed_initial_data(db: Session) -> None:
    now = datetime.now(timezone.utc)

    krojas = models.User(
        username="krojas",
        name="Kennedy Rojas",
        role="superadmin",
        password_hash=get_password_hash("krojas"),
    )
    mgomez = models.User(
        username="mgomez",
        name="Marcos Gomez",
        role="manager",
        password_hash=get_password_hash("mgomez"),
    )
    eguzman = models.User(
        username="eguzman",
        name="Estela Guzman",
        role="admin",
        password_hash=get_password_hash("eguzman"),
    )
    dhernandez = models.User(
        username="dhernandez",
        name="Diego Hernandez",
        role="admin",
        password_hash=get_password_hash("dhernandez"),
    )

    db.add_all([krojas, mgomez, eguzman, dhernandez])
    db.flush()

    torre_norte = models.Building(
        name="Torre Norte",
        address="Av. Principal 123",
        departments_count=40,
        admin_id=eguzman.id,
        imagen_frontis="/static/img/default-product.png",
    )
    edificio_central = models.Building(
        name="Edificio Central",
        address="Calle Florida 456",
        departments_count=60,
        admin_id=dhernandez.id,
        imagen_frontis="/static/img/default-product.png",
    )
    complejo_sur = models.Building(
        name="Complejo Sur",
        address="Ruta Nacional 789",
        departments_count=25,
        admin_id=eguzman.id,
        imagen_frontis="/static/img/default-product.png",
    )

    db.add_all([torre_norte, edificio_central, complejo_sur])
    db.flush()

    products = [
        models.Product(
            sku="LIM-001",
            name="Lejia",
            categoria="Limpieza",
            description="Lejia concentrada para desinfeccion general.",
            unit="Litro",
            precio=8.50,
            imagen_url="/static/img/default-product.png",
            stock_actual=42,
            stock_minimo=15,
        ),
        models.Product(
            sku="LIM-002",
            name="Escoba Industrial",
            categoria="Limpieza",
            description="Escoba de uso intensivo para exteriores e interiores.",
            unit="Unidad",
            precio=25.00,
            imagen_url="/static/img/default-product.png",
            stock_actual=18,
            stock_minimo=10,
        ),
        models.Product(
            sku="LIM-003",
            name="Papel Toalla",
            categoria="Insumos",
            description="Paquete absorbente de doble hoja.",
            unit="Paquete",
            precio=12.90,
            imagen_url="/static/img/default-product.png",
            stock_actual=9,
            stock_minimo=20,
        ),
        models.Product(
            sku="LIM-004",
            name="Detergente Multiusos",
            categoria="Limpieza",
            description="Galon multiusos con aroma neutro.",
            unit="Galon",
            precio=35.00,
            imagen_url="/static/img/default-product.png",
            stock_actual=27,
            stock_minimo=12,
        ),
        models.Product(
            sku="LIM-005",
            name="Bolsas de Basura",
            categoria="Insumos",
            description="Bolsas resistentes de 75 litros.",
            unit="Paquete",
            precio=18.50,
            imagen_url="/static/img/default-product.png",
            stock_actual=6,
            stock_minimo=18,
        ),
    ]

    db.add_all(products)
    db.flush()

    for product in products:
        db.add(
            models.InventoryMovement(
                product_id=product.id,
                quantity=product.stock_actual,
                movement_type="in",
                reference_id=None,
                created_by_id=krojas.id,
                created_at=now - timedelta(days=10),
            )
        )

    draft_order = models.Order(
        building_id=torre_norte.id,
        created_by_id=eguzman.id,
        created_at=now - timedelta(days=1),
        status="draft",
    )
    submitted_order = models.Order(
        building_id=torre_norte.id,
        created_by_id=eguzman.id,
        created_at=now - timedelta(hours=12),
        status="submitted",
    )
    processing_order = models.Order(
        building_id=edificio_central.id,
        created_by_id=dhernandez.id,
        created_at=now - timedelta(hours=8),
        status="processing",
    )
    dispatched_order = models.Order(
        building_id=complejo_sur.id,
        created_by_id=eguzman.id,
        created_at=now - timedelta(days=3),
        status="dispatched",
    )
    delivered_order = models.Order(
        building_id=edificio_central.id,
        created_by_id=dhernandez.id,
        created_at=now - timedelta(days=6),
        status="delivered",
    )

    db.add_all([draft_order, submitted_order, processing_order, dispatched_order, delivered_order])
    db.flush()

    order_items = [
        models.OrderItem(
            order_id=draft_order.id,
            product_id=products[0].id,
            quantity=4,
            nombre_producto_snapshot=products[0].name,
            precio_unitario=products[0].precio,
        ),
        models.OrderItem(
            order_id=draft_order.id,
            product_id=products[2].id,
            quantity=2,
            nombre_producto_snapshot=products[2].name,
            precio_unitario=products[2].precio,
        ),
        models.OrderItem(
            order_id=submitted_order.id,
            product_id=products[1].id,
            quantity=3,
            nombre_producto_snapshot=products[1].name,
            precio_unitario=products[1].precio,
        ),
        models.OrderItem(
            order_id=submitted_order.id,
            product_id=products[4].id,
            quantity=5,
            nombre_producto_snapshot=products[4].name,
            precio_unitario=products[4].precio,
        ),
        models.OrderItem(
            order_id=processing_order.id,
            product_id=products[0].id,
            quantity=6,
            nombre_producto_snapshot=products[0].name,
            precio_unitario=products[0].precio,
        ),
        models.OrderItem(
            order_id=processing_order.id,
            product_id=products[3].id,
            quantity=2,
            nombre_producto_snapshot=products[3].name,
            precio_unitario=products[3].precio,
        ),
        models.OrderItem(
            order_id=dispatched_order.id,
            product_id=products[2].id,
            quantity=8,
            nombre_producto_snapshot=products[2].name,
            precio_unitario=products[2].precio,
        ),
        models.OrderItem(
            order_id=dispatched_order.id,
            product_id=products[4].id,
            quantity=4,
            nombre_producto_snapshot=products[4].name,
            precio_unitario=products[4].precio,
        ),
        models.OrderItem(
            order_id=delivered_order.id,
            product_id=products[3].id,
            quantity=3,
            nombre_producto_snapshot=products[3].name,
            precio_unitario=products[3].precio,
        ),
    ]
    db.add_all(order_items)
    db.flush()

    pending_batch = models.DispatchBatch(
        created_by_id=mgomez.id,
        created_at=now - timedelta(hours=6),
        status="pending",
    )
    pending_batch.orders.append(processing_order)

    dispatched_batch = models.DispatchBatch(
        created_by_id=mgomez.id,
        created_at=now - timedelta(days=2),
        status="dispatched",
    )
    dispatched_batch.orders.append(dispatched_order)

    db.add_all([pending_batch, dispatched_batch])
    db.flush()

    db.add_all(
        [
            models.DispatchBatchItem(
                batch_id=pending_batch.id,
                product_id=products[0].id,
                total_quantity=6,
            ),
            models.DispatchBatchItem(
                batch_id=pending_batch.id,
                product_id=products[3].id,
                total_quantity=2,
            ),
            models.DispatchBatchItem(
                batch_id=dispatched_batch.id,
                product_id=products[2].id,
                total_quantity=8,
            ),
            models.DispatchBatchItem(
                batch_id=dispatched_batch.id,
                product_id=products[4].id,
                total_quantity=4,
            ),
        ]
    )

    db.add_all(
        [
            models.BuildingInventory(
                building_id=torre_norte.id,
                product_id=products[0].id,
                quantity=7,
            ),
            models.BuildingInventory(
                building_id=torre_norte.id,
                product_id=products[2].id,
                quantity=5,
            ),
            models.BuildingInventory(
                building_id=edificio_central.id,
                product_id=products[3].id,
                quantity=9,
            ),
        ]
    )

    db.add_all(
        [
            models.ConsumptionLog(
                building_id=torre_norte.id,
                product_id=products[0].id,
                reported_by_id=eguzman.id,
                quantity_consumed=2,
                reported_at=now - timedelta(days=2),
            ),
            models.ConsumptionLog(
                building_id=edificio_central.id,
                product_id=products[3].id,
                reported_by_id=dhernandez.id,
                quantity_consumed=1,
                reported_at=now - timedelta(days=1),
            ),
        ]
    )

    purchase = models.Purchase(
        supplier="Proveedor Central SAC",
        invoice_number="FAC-1001",
        purchase_date=date.today() - timedelta(days=4),
        total_amount=142.00,
        notes="Reposicion quincenal de insumos",
        created_by_id=mgomez.id,
        created_at=now - timedelta(days=4),
    )
    db.add(purchase)
    db.flush()

    db.add_all(
        [
            models.PurchaseItem(
                purchase_id=purchase.id,
                product_id=products[0].id,
                quantity=10,
                unit_price=products[0].precio,
            ),
            models.PurchaseItem(
                purchase_id=purchase.id,
                product_id=products[4].id,
                quantity=3,
                unit_price=products[4].precio,
            ),
        ]
    )

    db.commit()
