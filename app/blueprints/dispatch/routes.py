from flask import request, render_template, redirect, url_for, flash
from flask_login import current_user, login_required
from app.blueprints.dispatch import dispatch_bp
from app.models import Order, OrderItem, DispatchBatch, DispatchBatchItem, Product, InventoryMovement
from app.extensions import db
from app.utils.decorators import superadmin_required


@dispatch_bp.route('/pending')
@superadmin_required
def list_pending():
    """List all orders that are ready to be consolidated (draft or submitted)."""
    orders = Order.query.filter(Order.status.in_(['draft', 'submitted'])).order_by(Order.created_at.desc()).all()
    return render_template('dispatch/pending_orders.html', orders=orders)


@dispatch_bp.route('/consolidate', methods=['POST'])
@superadmin_required
def consolidate_orders():
    """Consolidate selected orders into a single DispatchBatch."""
    selected_order_ids = request.form.getlist('order_ids')

    if not selected_order_ids:
        flash('Por favor selecciona al menos un pedido para consolidar.', 'error')
        return redirect(url_for('dispatch.list_pending'))

    selected_order_ids = [int(id) for id in selected_order_ids]
    orders = Order.query.filter(Order.id.in_(selected_order_ids), Order.status.in_(['draft', 'submitted'])).all()

    if not orders:
        flash('Los pedidos seleccionados no son válidos.', 'error')
        return redirect(url_for('dispatch.list_pending'))

    batch = DispatchBatch(created_by_id=current_user.id, status='pending')
    db.session.add(batch)

    for order in orders:
        batch.orders.append(order)
        order.status = 'processing'

    db.session.flush()

    product_totals = {}
    for order in orders:
        for item in order.items:
            if item.product_id in product_totals:
                product_totals[item.product_id] += item.quantity
            else:
                product_totals[item.product_id] = item.quantity

    for product_id, total in product_totals.items():
        batch_item = DispatchBatchItem(
            batch_id=batch.id,
            product_id=product_id,
            total_quantity=total
        )
        db.session.add(batch_item)

    db.session.commit()
    flash(f'Lote de despacho #{batch.id} generado exitosamente. Se han consolidado {len(orders)} pedido(s).', 'success')
    return redirect(url_for('dispatch.batch_detail', batch_id=batch.id))


@dispatch_bp.route('/batch/<int:batch_id>')
@superadmin_required
def batch_detail(batch_id):
    """View the aggregated packing list for a given batch."""
    batch = DispatchBatch.query.get_or_404(batch_id)
    return render_template('dispatch/batch_detail.html', batch=batch)


@dispatch_bp.route('/picking/<int:batch_id>')
@superadmin_required
def picking(batch_id):
    """View the final picking list for warehouse staff to confirm dispatch."""
    batch = DispatchBatch.query.get_or_404(batch_id)

    if batch.status != 'pending':
        flash('Este lote ya ha sido despachado.', 'info')
        return redirect(url_for('dispatch.batch_detail', batch_id=batch.id))

    return render_template('dispatch/picking.html', batch=batch)


@dispatch_bp.route('/picking/<int:batch_id>/confirm', methods=['POST'])
@superadmin_required
def confirm_dispatch(batch_id):
    """Process the dispatch: deduct stock, change status, and log movements."""
    batch = DispatchBatch.query.get_or_404(batch_id)

    if batch.status != 'pending':
        flash('El lote no está pendiente.', 'error')
        return redirect(url_for('dispatch.batch_detail', batch_id=batch.id))

    for item in batch.items:
        product = Product.query.with_for_update().get(item.product_id)
        product.stock_actual -= item.total_quantity

        movement = InventoryMovement(
            product_id=product.id,
            quantity=item.total_quantity,
            movement_type='out',
            reference_id=batch.id,
            created_by_id=current_user.id
        )
        db.session.add(movement)

    batch.status = 'dispatched'

    for order in batch.orders:
        order.status = 'dispatched'

    db.session.commit()

    flash(f'¡Despacho completado! El inventario ha sido descontado para el Lote #{batch.id}.', 'success')
    return redirect(url_for('dispatch.batch_detail', batch_id=batch.id))
