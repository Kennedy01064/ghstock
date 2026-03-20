from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from app.blueprints.orders import orders_bp
from app.models import User, Building, Product, Order, OrderItem
from app.extensions import db
from app.utils.decorators import admin_required


# ─────────────────────────────────────────────────────────────────────────────
# IDOR helper: raises 403 if the given order does not belong to the current
# admin's assigned buildings.  Superadmins bypass this check.
# ─────────────────────────────────────────────────────────────────────────────
def _assert_order_ownership(order: Order):
    """Raise 403 if current_user has no right to touch this order."""
    if current_user.role == 'superadmin':
        return  # superadmins can see everything
    # Collect IDs of buildings assigned to this admin
    my_building_ids = {b.id for b in current_user.assigned_buildings}
    if order.building_id not in my_building_ids:
        abort(403)


# ─────────────────────────────────────────────────────────────────────────────
# List buildings assigned to the current admin
# ─────────────────────────────────────────────────────────────────────────────
@orders_bp.route('/buildings')
@admin_required
def list_buildings():
    """List buildings assigned to the current logged-in admin."""
    if current_user.role == 'superadmin':
        buildings = Building.query.all()
    else:
        buildings = Building.query.filter_by(admin_id=current_user.id).all()
    return render_template('orders/list_buildings.html', buildings=buildings, user=current_user)


# ─────────────────────────────────────────────────────────────────────────────
# Create a new draft order for a building
# ─────────────────────────────────────────────────────────────────────────────
@orders_bp.route('/create/<int:building_id>', methods=['POST'])
@admin_required
def create_order(building_id):
    """Create a new draft order for the selected building.
    IDOR: building must belong to the current admin.
    """
    # Only allow creating orders for buildings this admin owns (or any building if superadmin)
    if current_user.role == 'superadmin':
        building = Building.query.filter_by(id=building_id).first_or_404()
    else:
        building = Building.query.filter_by(id=building_id, admin_id=current_user.id).first_or_404()

    existing_draft = Order.query.filter_by(building_id=building.id, status='draft').first()
    if existing_draft:
        flash(f'Ya existe un pedido en borrador para {building.name}.', 'info')
        return redirect(url_for('orders.order_detail', order_id=existing_draft.id))

    new_order = Order(building_id=building.id, created_by_id=current_user.id, status='draft')
    db.session.add(new_order)
    db.session.commit()
    return redirect(url_for('orders.order_detail', order_id=new_order.id))


# ─────────────────────────────────────────────────────────────────────────────
# View the details of a specific order
# ─────────────────────────────────────────────────────────────────────────────
@orders_bp.route('/<int:order_id>')
@admin_required
def order_detail(order_id):
    """View the details of a specific order (draft) and allow adding products.
    IDOR: validates that the order's building belongs to current_user.
    """
    order = Order.query.get_or_404(order_id)
    _assert_order_ownership(order)
    products = Product.query.filter_by(is_active=True).order_by(Product.name).all()
    return render_template('orders/order_detail.html', order=order, products=products)


# ─────────────────────────────────────────────────────────────────────────────
# HTMX: Add an item to the order
# ─────────────────────────────────────────────────────────────────────────────
@orders_bp.route('/<int:order_id>/add_item', methods=['POST'])
@admin_required
def add_item(order_id):
    """HTMX endpoint to add an item to the order dynamically.
    IDOR: validates order ownership.
    State: order must still be in 'draft'.
    Snapshot: copies product name and price at the time of adding.
    """
    order = Order.query.get_or_404(order_id)
    _assert_order_ownership(order)

    # State machine guard
    if order.status != 'draft':
        abort(400)

    product_id = request.form.get('product_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    if quantity < 1:
        quantity = 1

    if product_id:
        product = Product.query.get_or_404(product_id)
        existing_item = OrderItem.query.filter_by(order_id=order.id, product_id=product_id).first()

        if existing_item:
            # Solo actualizar cantidad; pero también actualizar snapshot por si el precio cambió
            existing_item.quantity += quantity
            existing_item.precio_unitario = product.precio or 0.0
            existing_item.nombre_producto_snapshot = product.name
        else:
            new_item = OrderItem(
                order_id=order.id,
                product_id=product.id,
                quantity=quantity,
                # ── Snapshot: lock the name & price at this exact moment ──
                nombre_producto_snapshot=product.name,
                precio_unitario=product.precio or 0.0,
            )
            db.session.add(new_item)

        db.session.commit()

    return render_template('orders/partials/order_items.html', order=order)


# ─────────────────────────────────────────────────────────────────────────────
# HTMX: Remove an item from the order
# ─────────────────────────────────────────────────────────────────────────────
@orders_bp.route('/<int:order_id>/remove_item/<int:item_id>', methods=['POST'])
@admin_required
def remove_item(order_id, item_id):
    """HTMX endpoint to remove an item from the order.
    IDOR: validates order ownership.
    State: order must still be in 'draft'.
    """
    order = Order.query.get_or_404(order_id)
    _assert_order_ownership(order)

    if order.status != 'draft':
        abort(400)

    item = OrderItem.query.filter_by(id=item_id, order_id=order.id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return render_template('orders/partials/order_items.html', order=order)


# ─────────────────────────────────────────────────────────────────────────────
# Submit the order (draft → submitted)
# ─────────────────────────────────────────────────────────────────────────────
@orders_bp.route('/<int:order_id>/submit', methods=['POST'])
@admin_required
def submit_order(order_id):
    """Move an order from 'draft' to 'submitted'.
    IDOR: validates order ownership.
    State machine: rejects if order is already past 'draft' (idempotency guard).
    """
    order = Order.query.with_for_update().get_or_404(order_id)
    _assert_order_ownership(order)

    # ── State machine guard: prevent double-submission ────────────────────────
    if order.status != 'draft':
        flash('Este pedido ya fue enviado o está siendo procesado. No se puede volver a enviar.', 'error')
        return redirect(url_for('orders.order_detail', order_id=order.id))

    if not order.items:
        flash('No puedes confirmar un pedido vacío. Agrega al menos un producto.', 'error')
        return redirect(url_for('orders.order_detail', order_id=order.id))

    order.status = 'submitted'
    db.session.commit()
    flash(f'Pedido #{order.id} enviado correctamente. El almacén lo procesará pronto.', 'success')
    return redirect(url_for('dashboard.index'))


# ─────────────────────────────────────────────────────────────────────────────
# Reopen a submitted order for editing (submitted → draft)
# ─────────────────────────────────────────────────────────────────────────────
@orders_bp.route('/<int:order_id>/reopen', methods=['POST'])
@admin_required
def reopen_order(order_id):
    """Move an order from 'submitted' back to 'draft' so the admin can edit it."""
    order = Order.query.with_for_update().get_or_404(order_id)
    _assert_order_ownership(order)

    if order.status != 'submitted':
        flash('Solo puedes editar pedidos que tengan estado "Enviado/Submitted". Si ya está en proceso, comunícate con almacén.', 'error')
        return redirect(url_for('orders.order_detail', order_id=order.id))

    order.status = 'draft'
    db.session.commit()
    flash('El pedido se ha reabierto. Ahora puedes modificar las cantidades o agregar más productos.', 'info')
    return redirect(url_for('orders.order_detail', order_id=order.id))
