from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import current_user, login_required
from app.blueprints.orders import orders_bp
from app.models import User, Building, Product, Order, OrderItem, BuildingInventory, ConsumptionLog
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
    
    critical_inventory = BuildingInventory.query.join(Product).filter(
        BuildingInventory.building_id == order.building_id,
        BuildingInventory.quantity <= Product.stock_minimo,
        Product.is_active == True
    ).all()

    return render_template('orders/order_detail.html', order=order, products=products, critical_inventory=critical_inventory)

@orders_bp.route('/<int:order_id>/receive', methods=['POST'])
@admin_required
def receive_order(order_id):
    """Confirm receipt of a dispatched order and increase local building inventory."""
    order = Order.query.get_or_404(order_id)
    _assert_order_ownership(order)
    
    if order.status != 'dispatched':
        flash('Este pedido no está en estado despachado.', 'error')
        return redirect(url_for('dashboard.index'))
        
    order.status = 'delivered'
    
    # Increase local inventory
    for item in order.items:
        local_inv = BuildingInventory.query.filter_by(
            building_id=order.building_id,
            product_id=item.product_id
        ).first()
        
        if local_inv:
            local_inv.quantity += item.quantity
        else:
            new_local_inv = BuildingInventory(
                building_id=order.building_id,
                product_id=item.product_id,
                quantity=item.quantity
            )
            db.session.add(new_local_inv)

    db.session.commit()
    flash('¡Recepción confirmada! El stock ha ingresado a tu inventario local.', 'success')
    return redirect(url_for('dashboard.index'))


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


# ─────────────────────────────────────────────────────────────────────────────
# Local Inventory Phase 2
# ─────────────────────────────────────────────────────────────────────────────
@orders_bp.route('/my_inventory')
@admin_required
def my_inventory():
    """View local building inventory for the current admin."""
    if current_user.role == 'superadmin':
        my_buildings = Building.query.all()
    else:
        my_buildings = current_user.assigned_buildings
        
    building_ids = [b.id for b in my_buildings]
    
    # Get inventory for these buildings, grouped
    inventory = BuildingInventory.query.filter(BuildingInventory.building_id.in_(building_ids)).all()
    
    return render_template('orders/my_inventory.html', inventory=inventory)

@orders_bp.route('/consume/<int:inventory_id>', methods=['POST'])
@admin_required
def consume_inventory(inventory_id):
    """HTMX endpoint to report consumption of local inventory."""
    inv = BuildingInventory.query.get_or_404(inventory_id)
    
    if current_user.role != 'superadmin':
        my_building_ids = {b.id for b in current_user.assigned_buildings}
        if inv.building_id not in my_building_ids:
            abort(403)
            
    quantity = request.form.get('quantity', 1, type=int)
    if quantity < 1:
        quantity = 1
    if quantity > inv.quantity:
        quantity = inv.quantity
            
    if inv.quantity > 0:
        inv.quantity -= quantity
        
        log = ConsumptionLog(
            building_id=inv.building_id,
            product_id=inv.product_id,
            reported_by_id=current_user.id,
            quantity_consumed=quantity
        )
        db.session.add(log)
        db.session.commit()
        
    return render_template('orders/partials/inventory_card.html', inv=inv)


@orders_bp.route('/adjust_stock/<int:inventory_id>', methods=['POST'])
@admin_required
def adjust_stock(inventory_id):
    """HTMX endpoint to manually adjust stock (add or remove)."""
    inv = BuildingInventory.query.get_or_404(inventory_id)
    
    if current_user.role != 'superadmin':
        my_building_ids = {b.id for b in current_user.assigned_buildings}
        if inv.building_id not in my_building_ids:
            abort(403)
    
    action = request.form.get('action')
    quantity = request.form.get('quantity', 1, type=int)
    
    if quantity < 1:
        quantity = 1
    
    if action == 'add':
        inv.quantity += quantity
    elif action == 'remove':
        if inv.quantity >= quantity:
            inv.quantity -= quantity
        else:
            flash('No hay suficiente stock para remover.', 'error')
            return redirect(url_for('orders.my_inventory'))
    else:
        flash('Acción inválida.', 'error')
        return redirect(url_for('orders.my_inventory'))
    
    db.session.commit()
    flash(f'Stock {"agregado" if action == "add" else "removido"}: {quantity} unidades.', 'success')
    return redirect(url_for('orders.my_inventory'))


@orders_bp.route('/add_inventory', methods=['GET', 'POST'])
@admin_required
def add_inventory_item():
    """Add a new product to local building inventory."""
    if request.method == 'POST':
        product_id = request.form.get('product_id', type=int)
        building_id = request.form.get('building_id', type=int)
        quantity = request.form.get('quantity', 1, type=int)
        
        if current_user.role != 'superadmin':
            my_building_ids = {b.id for b in current_user.assigned_buildings}
            if building_id not in my_building_ids:
                abort(403)
        
        if not product_id or quantity < 1:
            flash('Datos inválidos.', 'error')
            return redirect(url_for('orders.add_inventory_item'))
        
        existing = BuildingInventory.query.filter_by(
            building_id=building_id,
            product_id=product_id
        ).first()
        
        if existing:
            existing.quantity += quantity
        else:
            new_inv = BuildingInventory(
                building_id=building_id,
                product_id=product_id,
                quantity=quantity
            )
            db.session.add(new_inv)
        
        db.session.commit()
        flash(f'Producto agregado al inventario del edificio.', 'success')
        return redirect(url_for('orders.my_inventory'))
    
    if current_user.role == 'superadmin':
        buildings = Building.query.all()
    else:
        buildings = current_user.assigned_buildings
    
    products = Product.query.filter_by(is_active=True).order_by(Product.name).all()
    return render_template('orders/add_inventory.html', buildings=buildings, products=products)

