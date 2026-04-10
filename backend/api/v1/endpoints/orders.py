from typing import Any, List, Optional
from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session, joinedload, selectinload
from backend import models, schemas
from backend.api import deps
from backend.services.order_service import OrderService

router = APIRouter()


@router.get("/", response_model=List[schemas.order.OrderDetail])
def read_orders(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    building_id: Optional[int] = None,
) -> Any:
    """List orders. Admin sees their buildings; superadmin/manager sees all."""
    if current_user.role in ("superadmin", "manager"):
        query = db.query(models.Order).options(
            selectinload(models.Order.items).joinedload(models.OrderItem.product),
            joinedload(models.Order.building),
            joinedload(models.Order.created_by),
        )
    else:
        my_building_ids = [b.id for b in current_user.assigned_buildings]
        query = db.query(models.Order).options(
            selectinload(models.Order.items).joinedload(models.OrderItem.product),
            joinedload(models.Order.building),
            joinedload(models.Order.created_by),
        ).filter(models.Order.building_id.in_(my_building_ids))

    if status:
        query = query.filter(models.Order.status == status)
    if building_id:
        query = query.filter(models.Order.building_id == building_id)

    return query.order_by(models.Order.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/consumption-report", response_model=List[schemas.order.ConsumptionReportRow])
def consumption_report(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    building_id: Optional[int] = None,
) -> Any:
    """Consumption logs grouped by building and product."""
    if current_user.role in ("superadmin", "manager"):
        building_ids = [b.id for b in db.query(models.Building).all()]
    else:
        building_ids = [b.id for b in current_user.assigned_buildings]

    q = db.query(
        models.Building.name.label("building_name"),
        models.Product.name.label("product_name"),
        models.Product.unit.label("unit"),
        models.Product.imagen_url.label("imagen_url"),
        func.sum(models.ConsumptionLog.quantity_consumed).label("total_consumed"),
        func.count(models.ConsumptionLog.id).label("events"),
        func.max(models.ConsumptionLog.reported_at).label("last_reported"),
    ).join(models.Building, models.ConsumptionLog.building_id == models.Building.id
    ).join(models.Product, models.ConsumptionLog.product_id == models.Product.id
    ).filter(models.ConsumptionLog.building_id.in_(building_ids))

    if building_id and building_id in building_ids:
        q = q.filter(models.ConsumptionLog.building_id == building_id)

    rows = q.group_by(
        models.Building.name, models.Product.name, models.Product.unit, models.Product.imagen_url
    ).order_by(func.sum(models.ConsumptionLog.quantity_consumed).desc()).all()

    return [
        schemas.order.ConsumptionReportRow(
            building_name=r.building_name,
            product_name=r.product_name,
            unit=r.unit,
            imagen_url=r.imagen_url,
            total_consumed=r.total_consumed,
            events=r.events,
            last_reported=r.last_reported,
        )
        for r in rows
    ]


@router.get("/{id}", response_model=schemas.order.OrderDetail)
def read_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get full order details."""
    service = OrderService(db, current_user)
    return service.get_order(id)


@router.post("/", response_model=schemas.order.Order)
def create_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: schemas.order.OrderCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Create a new draft order for a building."""
    service = OrderService(db, current_user)
    return service.create_order(order_in)


@router.post("/{id}/items", response_model=schemas.order.OrderItem)
def add_order_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.order.OrderItemCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Add item to order (draft only)."""
    service = OrderService(db, current_user)
    return service.add_order_item(id, item_in)


@router.delete("/{id}/items/{item_id}")
def remove_order_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Remove an item from a draft order."""
    service = OrderService(db, current_user)
    service.remove_order_item(id, item_id)
    return {"message": "Item removed"}


@router.post("/{id}/items/{item_id}/update", response_model=schemas.order.OrderItem)
def update_order_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_id: int,
    item_in: schemas.order.OrderItemUpdate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Update quantity of an existing item in a draft order."""
    service = OrderService(db, current_user)
    return service.update_order_item(id, item_id, item_in)


@router.post("/{id}/submit", response_model=schemas.order.Order)
def submit_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Submit the order (draft → submitted)."""
    service = OrderService(db, current_user)
    return service.submit_order(id)


@router.post("/{id}/reopen", response_model=schemas.order.Order)
def reopen_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Reopen a submitted order back to draft."""
    service = OrderService(db, current_user)
    return service.reopen_order(id)


@router.post("/{id}/cancel", response_model=schemas.order.Order)
def cancel_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Cancel a draft or submitted order."""
    service = OrderService(db, current_user)
    return service.cancel_order(id)


@router.post("/{id}/receive", response_model=schemas.order.Order)
def receive_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Confirm receipt of a dispatched order and update building inventory."""
    service = OrderService(db, current_user)
    return service.receive_order(id)


@router.post("/{id}/approve", response_model=schemas.order.Order)
def approve_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Approve a submitted order (submitted → approved)."""
    service = OrderService(db, current_user)
    return service.approve_order(id)


@router.post("/{id}/reject", response_model=schemas.order.Order)
def reject_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Reject a submitted order (submitted → rejected)."""
    service = OrderService(db, current_user)
    return service.reject_order(id)
