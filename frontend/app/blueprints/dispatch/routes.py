import csv
import io
from flask import request, render_template, redirect, url_for, flash, Response
from flask_login import current_user, login_required
from app.blueprints.dispatch import dispatch_bp
from app.models import Order, OrderItem, DispatchBatch, DispatchBatchItem, Product, InventoryMovement, BuildingInventory, Purchase, PurchaseItem
from app.extensions import db
from app.utils.decorators import management_required


@dispatch_bp.route('/pending')
@management_required
def list_pending():
    """List all orders that are ready to be consolidated (draft or submitted)."""
    orders = Order.query.filter(Order.status.in_(['draft', 'submitted'])).order_by(Order.created_at.desc()).all()
    return render_template('dispatch/pending_orders.html', orders=orders)


@dispatch_bp.route('/consolidate', methods=['POST'])
@management_required
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
@management_required
def batch_detail(batch_id):
    """View the aggregated packing list for a given batch."""
    batch = DispatchBatch.query.get_or_404(batch_id)
    return render_template('dispatch/batch_detail.html', batch=batch)


@dispatch_bp.route('/picking/<int:batch_id>')
@management_required
def picking(batch_id):
    """View the final picking list for warehouse staff to confirm dispatch."""
    batch = DispatchBatch.query.get_or_404(batch_id)

    if batch.status != 'pending':
        flash('Este lote ya ha sido despachado.', 'info')
        return redirect(url_for('dispatch.batch_detail', batch_id=batch.id))

    return render_template('dispatch/picking.html', batch=batch)


@dispatch_bp.route('/picking/<int:batch_id>/confirm', methods=['POST'])
@management_required
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

    flash(f'¡Despacho completado! El inventario ha sido descontado del almacén central y los pedidos están en tránsito.', 'success')
    return redirect(url_for('dispatch.batch_detail', batch_id=batch.id))

@dispatch_bp.route('/batch/<int:batch_id>/export/consolidated')
@management_required
def export_batch(batch_id):
    """Export the batch picking list to PDF."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    import io

    batch = DispatchBatch.query.get_or_404(batch_id)

    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    elements.append(Paragraph(f"Consolidado de Productos - Lote #{batch_id}", title_style))
    elements.append(Spacer(1, 12))

    data = [['SKU', 'Producto', 'Unidad', 'Cantidad Total']]
    for item in batch.items:
        data.append([
            item.product.sku or 'N/A',
            Paragraph(item.product.name, styles['Normal']),
            item.product.unit,
            str(item.total_quantity)
        ])

    table = Table(data, colWidths=[80, 250, 80, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.grey),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (1,1), (1,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    pdf_data = output.getvalue()
    output.close()
    
    return Response(
        pdf_data,
        mimetype='application/pdf',
        headers={"Content-Disposition": f'attachment; filename="consolidado_lote_{batch_id}.pdf"'}
    )

@dispatch_bp.route('/batch/<int:batch_id>/export/buildings')
@management_required
def export_batch_buildings(batch_id):
    """Export the batch picking list separated by building to PDF."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet
    import io

    batch = DispatchBatch.query.get_or_404(batch_id)

    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    elements = []
    
    styles = getSampleStyleSheet()
    title_style = styles['Heading1']
    elements.append(Paragraph(f"Distribución por Edificios - Lote #{batch_id}", title_style))
    elements.append(Spacer(1, 12))

    data = [['Edificio', 'SKU', 'Producto', 'Unidad', 'Cant.', 'Precio', 'Total']]
    for order in batch.orders:
        building_name = order.building.name
        for item in order.items:
            price = item.precio_unitario if item.precio_unitario is not None else item.product.precio
            name = item.nombre_producto_snapshot or item.product.name
            total = item.quantity * price
            
            data.append([
                Paragraph(building_name, styles['Normal']),
                item.product.sku or 'N/A',
                Paragraph(name, styles['Normal']),
                item.product.unit,
                str(item.quantity),
                f"S/{price:.2f}",
                f"S/{total:.2f}"
            ])

    table = Table(data, colWidths=[100, 50, 180, 50, 40, 50, 60])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.steelblue),
        ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('ALIGN', (0,1), (0,-1), 'LEFT'),
        ('ALIGN', (2,1), (2,-1), 'LEFT'),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('GRID', (0,0), (-1,-1), 1, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
    ]))
    
    elements.append(table)
    doc.build(elements)
    
    pdf_data = output.getvalue()
    output.close()
    
    return Response(
        pdf_data,
        mimetype='application/pdf',
        headers={"Content-Disposition": f'attachment; filename="distribucion_edificios_lote_{batch_id}.pdf"'}
    )

@dispatch_bp.route('/history')
@management_required
def history():
    """View historical dispatch batches processed by managers."""
    # Show only dispatched batches, reverse chronological order
    batches = DispatchBatch.query.filter_by(status='dispatched').order_by(DispatchBatch.created_at.desc()).all()
    return render_template('dispatch/history.html', batches=batches)


@dispatch_bp.route('/purchases')
@management_required
def list_purchases():
    """List all direct purchases (compras directas)."""
    purchases = Purchase.query.order_by(Purchase.purchase_date.desc()).all()
    return render_template('dispatch/purchases/list.html', purchases=purchases)


@dispatch_bp.route('/purchases/new', methods=['GET', 'POST'])
@management_required
def create_purchase():
    """Create a new direct purchase entry."""
    if request.method == 'POST':
        supplier = request.form.get('supplier', '').strip()
        invoice_number = request.form.get('invoice_number', '').strip()
        purchase_date_str = request.form.get('purchase_date', '').strip()
        notes = request.form.get('notes', '').strip()

        from datetime import datetime
        try:
            purchase_date = datetime.strptime(purchase_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Fecha inválida. Use formato YYYY-MM-DD', 'error')
            return redirect(url_for('dispatch.create_purchase'))

        product_ids = request.form.getlist('product_ids')
        quantities = request.form.getlist('quantities')
        unit_prices = request.form.getlist('unit_prices')

        if not product_ids:
            flash('Debe agregar al menos un producto.', 'error')
            return redirect(url_for('dispatch.create_purchase'))

        total_amount = 0.0
        purchase = Purchase(
            supplier=supplier if supplier else None,
            invoice_number=invoice_number if invoice_number else None,
            purchase_date=purchase_date,
            notes=notes if notes else None,
            created_by_id=current_user.id
        )
        db.session.add(purchase)
        db.session.flush()

        for i, prod_id in enumerate(product_ids):
            if not prod_id:
                continue
            qty = int(quantities[i]) if i < len(quantities) and quantities[i] else 1
            unit_price = float(unit_prices[i]) if i < len(unit_prices) and unit_prices[i] else 0.0

            if qty <= 0:
                continue

            product = Product.query.get(prod_id)
            if not product:
                continue

            purchase_item = PurchaseItem(
                purchase_id=purchase.id,
                product_id=product.id,
                quantity=qty,
                unit_price=unit_price
            )
            db.session.add(purchase_item)

            product.stock_actual += qty

            movement = InventoryMovement(
                product_id=product.id,
                quantity=qty,
                movement_type='in',
                reference_id=purchase.id,
                created_by_id=current_user.id
            )
            db.session.add(movement)

            total_amount += qty * unit_price

        purchase.total_amount = total_amount
        db.session.commit()

        flash(f'Compra registrada correctamente. Stock actualizado.', 'success')
        return redirect(url_for('dispatch.list_purchases'))

    products = Product.query.filter_by(is_active=True).order_by(Product.name).all()
    return render_template('dispatch/purchases/create.html', products=products)


@dispatch_bp.route('/purchases/<int:purchase_id>')
@management_required
def purchase_detail(purchase_id):
    """View details of a specific purchase."""
    purchase = Purchase.query.get_or_404(purchase_id)
    return render_template('dispatch/purchases/detail.html', purchase=purchase)
