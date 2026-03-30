from flask import render_template, session
from flask_login import current_user, login_required
from datetime import datetime, timezone
from sqlalchemy import func
from app.blueprints.dashboard import dashboard_bp
from app.models import Order, OrderItem, Building, Product, DispatchBatch, DispatchBatchItem, BuildingInventory
from app.extensions import db
from app.utils.decorators import superadmin_required


@dashboard_bp.route('/')
@login_required
def index():
    """Main hub: renders superadmin analytics OR admin operations panel, based on role."""

    # ── Admin route: show the admin's operational dashboard ──
    if current_user.role == 'admin' or session.get('view_as_admin'):
        if current_user.role == 'superadmin':
            # Superadmin seeing as admin: sees all buildings and all global orders
            buildings = Building.query.all()
            pedidos_activos = Order.query.filter(
                Order.status.in_(['draft', 'submitted', 'processing'])
            ).count()
            pedidos_en_transito = Order.query.filter(
                Order.status.in_(['submitted', 'processing'])
            ).count()
            historial_pedidos = Order.query.order_by(Order.created_at.desc()).limit(10).all()
        else:
            # Normal admin view: scoped to their ID
            buildings = Building.query.filter_by(admin_id=current_user.id).all()
            pedidos_activos = Order.query.filter(
                Order.created_by_id == current_user.id,
                Order.status.in_(['draft', 'submitted', 'processing'])
            ).count()
            pedidos_en_transito = Order.query.filter(
                Order.created_by_id == current_user.id,
                Order.status.in_(['submitted', 'processing'])
            ).count()
            historial_pedidos = Order.query.filter_by(
                created_by_id=current_user.id
            ).order_by(Order.created_at.desc()).limit(10).all()

        return render_template('dashboard/admin_dashboard.html',
            buildings=buildings,
            pedidos_activos=pedidos_activos,
            pedidos_en_transito=pedidos_en_transito,
            historial_pedidos=historial_pedidos
        )

    # ── Superadmin route: full analytics dashboard ──
    total_pedidos_pendientes = Order.query.filter(
        Order.status.in_(['draft', 'submitted'])
    ).count()

    total_edificios_activos = db.session.query(
        func.count(func.distinct(Order.building_id))
    ).scalar() or 0

    now = datetime.now(timezone.utc)
    first_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    costo_despachado_mes = db.session.query(
        func.coalesce(func.sum(DispatchBatchItem.total_quantity * Product.precio), 0)
    ).join(
        Product, DispatchBatchItem.product_id == Product.id
    ).join(
        DispatchBatch, DispatchBatchItem.batch_id == DispatchBatch.id
    ).filter(
        DispatchBatch.status == 'dispatched',
        DispatchBatch.created_at >= first_of_month
    ).scalar() or 0

    total_productos = Product.query.count()

    alertas_stock = Product.query.filter(
        Product.stock_actual <= Product.stock_minimo
    ).order_by(Product.stock_actual.asc()).all()

    alertas_edificios = db.session.query(BuildingInventory).join(Product).filter(
        BuildingInventory.quantity <= Product.stock_minimo
    ).all()

    costos_por_edificio = db.session.query(
        Building.name,
        func.coalesce(func.sum(OrderItem.quantity * OrderItem.precio_unitario), 0).label('gasto_total')
    ).join(
        Order, Building.id == Order.building_id
    ).join(
        OrderItem, Order.id == OrderItem.order_id
    ).filter(
        Order.status.in_(['dispatched', 'delivered'])
    ).group_by(Building.name).order_by(db.text('gasto_total DESC')).all()

    pedidos_por_edificio = db.session.query(
        Building.name,
        func.count(Order.id).label('total_pedidos')
    ).join(
        Order, Building.id == Order.building_id
    ).group_by(Building.name).order_by(func.count(Order.id).desc()).all()

    chart_edificios_labels = [row[0] for row in pedidos_por_edificio]
    chart_edificios_data   = [row[1] for row in pedidos_por_edificio]

    top_productos = db.session.query(
        Product.name,
        func.sum(OrderItem.quantity).label('total_solicitado')
    ).join(
        OrderItem, Product.id == OrderItem.product_id
    ).group_by(Product.name).order_by(
        func.sum(OrderItem.quantity).desc()
    ).limit(5).all()

    chart_productos_labels = [row[0] for row in top_productos]
    chart_productos_data   = [int(row[1]) for row in top_productos]

    lotes_recientes = DispatchBatch.query.order_by(
        DispatchBatch.created_at.desc()
    ).limit(5).all()

    return render_template('dashboard/index.html',
        total_pedidos_pendientes=total_pedidos_pendientes,
        total_edificios_activos=total_edificios_activos,
        costo_despachado_mes=costo_despachado_mes,
        total_productos=total_productos,
        alertas_stock=alertas_stock,
        alertas_edificios=alertas_edificios,
        costos_por_edificio=costos_por_edificio,
        chart_edificios_labels=chart_edificios_labels,
        chart_edificios_data=chart_edificios_data,
        chart_productos_labels=chart_productos_labels,
        chart_productos_data=chart_productos_data,
        lotes_recientes=lotes_recientes
    )
