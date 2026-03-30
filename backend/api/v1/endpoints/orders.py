from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.order.Order])
def read_orders(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve orders.
    Admin sees their building orders, Superadmin sees all.
    """
    if current_user.role == "superadmin":
        orders = db.query(models.Order).offset(skip).limit(limit).all()
    else:
        # Collect IDs of buildings assigned to this admin
        my_building_ids = [b.id for b in current_user.assigned_buildings]
        orders = db.query(models.Order).filter(models.Order.building_id.in_(my_building_ids)).all()
    return orders

@router.post("/", response_model=schemas.order.Order)
def create_order(
    *,
    db: Session = Depends(deps.get_db),
    order_in: schemas.order.OrderCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new draft order for a building.
    """
    # Verify ownership
    if current_user.role != "superadmin":
        building = db.query(models.Building).filter(
            models.Building.id == order_in.building_id, 
            models.Building.admin_id == current_user.id
        ).first()
        if not building:
            raise HTTPException(status_code=403, detail="Not enough privileges for this building")

    existing_draft = db.query(models.Order).filter(
        models.Order.building_id == order_in.building_id, 
        models.Order.status == "draft"
    ).first()
    
    if existing_draft:
        return existing_draft

    order = models.Order(
        building_id=order_in.building_id,
        created_by_id=current_user.id,
        status="draft"
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

@router.post("/{id}/items", response_model=schemas.order.OrderItem)
def add_order_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.order.OrderItemCreate,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Add item to order (draft only).
    Does product snapshotting.
    """
    order = db.query(models.Order).filter(models.Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status != "draft":
        raise HTTPException(status_code=400, detail="Order is not in draft status")

    # Ownership check
    if current_user.role != "superadmin":
        if order.building.admin_id != current_user.id:
            raise HTTPException(status_code=403, detail="Forbidden")

    product = db.query(models.Product).filter(models.Product.id == item_in.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    existing_item = db.query(models.OrderItem).filter(
        models.OrderItem.order_id == id, 
        models.OrderItem.product_id == item_in.product_id
    ).first()

    if existing_item:
        existing_item.quantity += item_in.quantity
        existing_item.precio_unitario = product.precio or 0.0
        existing_item.nombre_producto_snapshot = product.name
        db.commit()
        db.refresh(existing_item)
        return existing_item
    else:
        new_item = models.OrderItem(
            order_id=id,
            product_id=product.id,
            quantity=item_in.quantity,
            nombre_producto_snapshot=product.name,
            precio_unitario=product.precio or 0.0
        )
        db.add(new_item)
        db.commit()
        db.refresh(new_item)
        return new_item

@router.post("/{id}/submit", response_model=schemas.order.Order)
def submit_order(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Submit the order (draft -> submitted).
    """
    order = db.query(models.Order).filter(models.Order.id == id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.status != "draft":
        raise HTTPException(status_code=400, detail="Only draft orders can be submitted")
    
    if not order.items:
        raise HTTPException(status_code=400, detail="Cannot submit empty order")

    order.status = "submitted"
    db.commit()
    db.refresh(order)
    return order
