from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.api import deps
from datetime import datetime

router = APIRouter()

@router.get("/pending-orders", response_model=List[schemas.order.Order])
def read_pending_orders(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superadmin),
) -> Any:
    """
    List all orders ready for consolidation (submitted).
    """
    orders = db.query(models.Order).filter(models.Order.status == "submitted").all()
    return orders

@router.post("/consolidate", response_model=schemas.order.Order) # Change return type if needed
def consolidate_orders(
    *,
    db: Session = Depends(deps.get_db),
    order_ids: List[int],
    current_user: models.User = Depends(deps.get_current_active_superadmin),
) -> Any:
    """
    Consolidate multiple orders into a DispatchBatch.
    """
    orders = db.query(models.Order).filter(
        models.Order.id.in_(order_ids), 
        models.Order.status == "submitted"
    ).all()
    
    if not orders:
        raise HTTPException(status_code=400, detail="No valid submitted orders found")

    batch = models.DispatchBatch(created_by_id=current_user.id, status="pending")
    db.add(batch)
    db.flush()

    product_totals = {}
    for order in orders:
        batch.orders.append(order)
        order.status = "processing"
        for item in order.items:
            product_totals[item.product_id] = product_totals.get(item.product_id, 0) + item.quantity

    for product_id, total in product_totals.items():
        batch_item = models.DispatchBatchItem(
            batch_id=batch.id,
            product_id=product_id,
            total_quantity=total
        )
        db.add(batch_item)

    db.commit()
    db.refresh(batch)
    return {"message": f"Batch #{batch.id} created with {len(orders)} orders"}

@router.post("/batch/{id}/confirm")
def confirm_dispatch(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superadmin),
) -> Any:
    """
    Confirm dispatch: deduct stock from central and log movements.
    """
    batch = db.query(models.DispatchBatch).filter(models.DispatchBatch.id == id).first()
    if not batch or batch.status != "pending":
        raise HTTPException(status_code=400, detail="Invalid batch or status")

    for item in batch.items:
        product = db.query(models.Product).filter(models.Product.id == item.product_id).with_for_update().first()
        if not product:
            continue
        product.stock_actual -= item.total_quantity
        
        movement = models.InventoryMovement(
            product_id=product.id,
            quantity=item.total_quantity,
            movement_type="out",
            reference_id=batch.id,
            created_by_id=current_user.id
        )
        db.add(movement)

    batch.status = "dispatched"
    for order in batch.orders:
        order.status = "dispatched"

    db.commit()
    return {"message": "Dispatch confirmed and stock updated"}
