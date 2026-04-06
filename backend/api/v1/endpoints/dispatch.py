import io
from typing import Any, List
from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.api import deps
from backend.services.dispatch_service import DispatchService
from backend.services.purchase_service import PurchaseService
from backend.domain.constants import BatchStatus, OrderStatus

router = APIRouter()


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
    elements = [
        Paragraph(f"Consolidado de Productos - Lote #{id}", styles["Heading1"]),
        Spacer(1, 12),
    ]

    data = [["SKU", "Producto", "Unidad", "Cantidad Total"]]
    for item in batch.items:
        data.append([
            item.product.sku or "N/A",
            Paragraph(item.product.name, styles["Normal"]),
            item.product.unit,
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

    batch = db.query(models.DispatchBatch).filter(models.DispatchBatch.id == id).first()
    if not batch:
        raise HTTPException(status_code=404, detail="Batch not found")

    output = io.BytesIO()
    doc = SimpleDocTemplate(output, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = [
        Paragraph(f"Distribución por Edificios - Lote #{id}", styles["Heading1"]),
        Spacer(1, 12),
    ]

    data = [["Edificio", "SKU", "Producto", "Unidad", "Cant.", "Precio", "Total"]]
    for order in batch.orders:
        building_name = order.building.name
        for item in order.items:
            price = item.precio_unitario if item.precio_unitario is not None else item.product.precio
            name = item.nombre_producto_snapshot or item.product.name
            total = item.quantity * price
            data.append([
                Paragraph(building_name, styles["Normal"]),
                item.product.sku or "N/A",
                Paragraph(name, styles["Normal"]),
                item.product.unit,
                str(item.quantity),
                f"S/{price:.2f}",
                f"S/{total:.2f}",
            ])

    table = Table(data, colWidths=[100, 50, 180, 50, 40, 50, 60])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.steelblue),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
        ("ALIGN", (0, 1), (0, -1), "LEFT"),
        ("ALIGN", (2, 1), (2, -1), "LEFT"),
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
        headers={"Content-Disposition": f"attachment; filename=distribucion_edificios_lote_{id}.pdf"},
    )


@router.get("/purchases/", response_model=List[schemas.dispatch.PurchaseDetail])
def list_purchases(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_management),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """List purchases. Paginated: use skip and limit query parameters."""
    return (
        db.query(models.Purchase)
        .order_by(models.Purchase.purchase_date.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


@router.post("/purchases/", response_model=schemas.dispatch.PurchaseDetail)
def create_purchase(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    purchase_in: schemas.dispatch.PurchaseCreate,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Create a new purchase and update central stock."""
    # Note: delegates to PurchaseService for atomic stock intake and audit logging.
    # Public contract (URL, request/response shape) is unchanged.
    request_id = getattr(request.state, "request_id", "unknown")
    # Map schemas.dispatch.PurchaseCreate → schemas.purchase.PurchaseCreate
    purchase_create = schemas.purchase.PurchaseCreate(
        supplier=purchase_in.supplier,
        invoice_number=purchase_in.invoice_number,
        purchase_date=purchase_in.purchase_date,
        notes=purchase_in.notes,
        items=[
            schemas.purchase.PurchaseItemCreate(
                product_id=item.product_id,
                quantity=item.quantity,
                unit_price=item.unit_price,
            )
            for item in purchase_in.items
        ]
    )
    return PurchaseService.create_purchase(
        db=db,
        purchase_in=purchase_create,
        actor_id=current_user.id,
        request_id=request_id,
    )


@router.get("/purchases/{id}", response_model=schemas.dispatch.PurchaseDetail)
def get_purchase(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Get purchase detail."""
    purchase = db.query(models.Purchase).filter(models.Purchase.id == id).first()
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase
