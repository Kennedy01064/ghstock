import io
import os
from datetime import datetime
from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.api import deps
from backend.services.dispatch_service import DispatchService
from backend.services.purchase_service import PurchaseService
from backend.domain.constants import BatchStatus, OrderStatus
from xml.sax.saxutils import escape as xml_escape

router = APIRouter()

def get_pdf_header_elements(title: str, batch: models.DispatchBatch, current_user: models.User, styles):
    from reportlab.lib import colors
    from reportlab.platypus import Table, TableStyle, Paragraph, Spacer, Image
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_RIGHT, TA_CENTER
    
    right_align_style = ParagraphStyle(name="RightAlign", parent=styles["Normal"], alignment=TA_RIGHT)
    title_style = ParagraphStyle(name="TitleStyle", parent=styles["Heading1"], alignment=TA_CENTER, textColor=colors.HexColor("#0f172a"))
    
    logo_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../../../../frontend-spa/public/static/img/logo_trans.png")
    
    if os.path.exists(logo_path):
        # We specify width and height in the constructor to ensure it fits in the table cell
        img = Image(logo_path, width=50, height=50)
        img.hAlign = 'LEFT'
        left_header = img
    else:
        left_header = Paragraph("<b>GRUPO HERNÁNDEZ</b>", styles["Normal"])
        
    company_info = """
    <b>GRUPO HERNÁNDEZ S.A.C.</b><br/>
    RUC: 20543219876<br/>
    Lima - Perú<br/>
    """
    right_header = Paragraph(company_info, right_align_style)
    
    header_table = Table([[left_header, right_header]], colWidths=[270, 270])
    header_table.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ALIGN', (0,0), (0,0), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'RIGHT'),
    ]))
    
    elements = [
        header_table,
        Spacer(1, 15),
        Paragraph(title, title_style),
        Spacer(1, 15),
    ]
    
    # Meta info table
    status_str = getattr(batch.status, 'value', str(batch.status)).upper()
    generator = current_user.name or current_user.username
    
    meta_info_data = [
        [
            Paragraph("<b>Lote de Despacho:</b>", styles["Normal"]), Paragraph(f"#{batch.id}", styles["Normal"]), 
            Paragraph("<b>Fecha de Emisión:</b>", styles["Normal"]), Paragraph(datetime.now().strftime("%d/%m/%Y %H:%M"), styles["Normal"])
        ],
        [
            Paragraph("<b>Estado:</b>", styles["Normal"]), Paragraph(status_str, styles["Normal"]), 
            Paragraph("<b>Generado por:</b>", styles["Normal"]), Paragraph(generator, styles["Normal"])
        ],
    ]
    
    meta_table = Table(meta_info_data, colWidths=[100, 170, 100, 170])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#f8fafc")),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('PADDING', (0,0), (-1,-1), 6),
    ]))
    
    elements.extend([meta_table, Spacer(1, 20)])
    
    return elements

@router.get("/pending-orders", response_model=List[schemas.order.OrderDetail])
def read_pending_orders(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """List all submitted orders ready for consolidation."""
    orders = db.query(models.Order).filter(models.Order.status == OrderStatus.SUBMITTED).all()
    return orders


@router.post("/consolidate")
def consolidate_orders(
    *,
    db: Session = Depends(deps.get_db),
    order_ids: List[int] = Body(...),
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Consolidate multiple submitted orders into a DispatchBatch."""
    service = DispatchService(db, current_user)
    return service.consolidate_orders(order_ids)


@router.get("/history", response_model=schemas.dispatch.DispatchHistoryResponse)
def get_history(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Historial: dispatched batches and all non-draft orders."""
    batches = db.query(models.DispatchBatch).filter(
        models.DispatchBatch.status == BatchStatus.DISPATCHED
    ).order_by(models.DispatchBatch.created_at.desc()).all()

    orders = db.query(models.Order).filter(
        models.Order.status != OrderStatus.DRAFT
    ).order_by(models.Order.created_at.desc()).all()

    return {"batches": batches, "orders": orders}


@router.get("/batch/{id}", response_model=schemas.dispatch.DispatchBatchDetail)
def get_batch_detail(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Get full detail of a dispatch batch."""
    batch = db.query(models.DispatchBatch).filter(models.DispatchBatch.id == id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return batch


@router.get("/batch/{id}/picking")
def get_picking_list(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Get the picking list for a pending batch."""
    batch = db.query(models.DispatchBatch).filter(models.DispatchBatch.id == id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")
    return {
        "batch_id": batch.id,
        "items": [
            {
                "product_id": item.product_id,
                "product_name": item.product.name,
                "sku": item.product.sku,
                "unit": item.product.unit,
                "total_quantity": item.total_quantity,
                "stock_actual": item.product.stock_actual,
            }
            for item in batch.items
        ],
    }


@router.post("/batch/{id}/confirm")
def confirm_dispatch(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Confirm dispatch: validate stock, deduct from central, mark orders dispatched."""
    service = DispatchService(db, current_user)
    service.confirm_dispatch(id)
    return {"message": "Dispatch confirmed and stock updated"}


@router.post("/batch/{id}/reject-order/{order_id}")
def reject_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    order_id: int,
    rejection_note: str = "",
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Return an order from a pending batch back to submitted with a rejection note."""
    service = DispatchService(db, current_user)
    service.reject_order(id, order_id, rejection_note)
    return {"message": f"Order #{order_id} returned to admin with rejection note"}


@router.get("/batch/{id}/export/consolidated")
def export_batch_consolidated(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Export consolidated picking list as PDF."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    batch = db.query(models.DispatchBatch).filter(models.DispatchBatch.id == id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    
    elements = get_pdf_header_elements(f"Consolidado de Productos - Lote #{id}", batch, current_user, styles)

    data = [["SKU", "Producto", "Unidad", "Cantidad Total"]]
    for item in batch.items:
        p_name = item.product.name if item.product else "Producto Desconocido"
        data.append([
            (item.product.sku if item.product else "N/A") or "N/A",
            Paragraph(xml_escape(p_name), styles["Normal"]),
            (item.product.unit if item.product else "u") or "u",
            str(item.total_quantity),
        ])

    table = Table(data, colWidths=[80, 250, 80, 100])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (1, 1), (1, -1), "LEFT"),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    elements.append(table)
    doc.build(elements)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=consolidado_lote_{id}.pdf"},
    )


@router.get("/batch/{id}/export/buildings")
def export_batch_buildings(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Export per-building picking list as PDF."""
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
    from reportlab.lib.styles import getSampleStyleSheet

    from collections import defaultdict

    batch = db.query(models.DispatchBatch).filter(models.DispatchBatch.id == id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    
    elements = get_pdf_header_elements(f"Distribución por Edificios - Lote #{id}", batch, current_user, styles)

    data = [["Edificio", "SKU", "Producto", "Unidad", "Cant.", "Precio", "Total"]]
    # Group items by building name
    building_groups = defaultdict(list)
    for order in batch.orders:
        b_name = order.building.name if order.building else "Sin Edificio"
        building_groups[b_name].extend(order.items)

    grand_total = 0

    for b_name, items in sorted(building_groups.items()):
        b_display_name = b_name if b_name else "Sin Edificio"
        # Agregar un título para el edificio
        elements.append(Paragraph(f"Edificio: {xml_escape(b_display_name)}", styles["Heading2"]))
        elements.append(Spacer(1, 6))

        # Tabla individual para el edificio
        data = [["SKU", "Producto", "Unidad", "Cant.", "Precio", "Total"]]
        building_subtotal = 0
        
        # Agrupar items por producto dentro del edificio para evitar duplicados si hay múltiples órdenes
        aggregated = {}
        for item in items:
            if not item.product:
                continue
            name = item.nombre_producto_snapshot or item.product.name
            # Fallback for price: snapshot -> product -> 0
            price = item.precio_unitario if item.precio_unitario is not None else (item.product.precio if item.product.precio is not None else 0)
            key = (item.product.sku, name, item.product.unit, price)
            if key not in aggregated:
                aggregated[key] = 0
            aggregated[key] += item.quantity
            
        for (sku, name, unit, price), quantity in aggregated.items():
            total = quantity * price
            building_subtotal += total
            
            data.append([
                sku or "N/A",
                Paragraph(xml_escape(name), styles["Normal"]),
                unit or "u",
                str(quantity),
                f"S/{price:.2f}",
                f"S/{total:.2f}",
            ])
            
        # Añadir subtotal
        data.append([
            "SUBTOTAL",
            "", "", "", "",
            f"S/{building_subtotal:.2f}"
        ])
        grand_total += building_subtotal

        # Crear tabla y estilos
        table = Table(data, colWidths=[70, 210, 60, 50, 60, 70])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.steelblue),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("ALIGN", (1, 1), (1, -1), "LEFT"),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
            ("GRID", (0, 0), (-1, -1), 1, colors.black),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            # Estilos del subtotal (última fila)
            ("BACKGROUND", (0, -1), (-1, -1), colors.lightgrey),
            ("FONTNAME", (0, -1), (-1, -1), "Helvetica-Bold"),
            ("SPAN", (0, -1), (4, -1)),
            ("ALIGN", (0, -1), (0, -1), "RIGHT"),
        ]))
        elements.append(table)
        elements.append(Spacer(1, 15))

    # Add Grand Total at the end
    grand_data = [["TOTAL GENERAL (TODOS LOS EDIFICIOS)", f"S/{grand_total:.2f}"]]
    grand_table = Table(grand_data, colWidths=[450, 70])
    grand_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("ALIGN", (0, 0), (0, 0), "RIGHT"),
        ("ALIGN", (1, 0), (1, 0), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 1, colors.black),
        ("BOTTOMPADDING", (0, 0), (-1, 0), 6),
    ]))
    elements.append(grand_table)
    doc.build(elements)
    output.seek(0)

    return StreamingResponse(
        output,
        media_type="application/pdf",
        headers={"Content-Disposition": f"attachment; filename=distribucion_edificios_lote_{id}.pdf"},
    )


