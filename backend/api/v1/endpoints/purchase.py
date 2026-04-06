from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from backend import models, schemas
from backend.api import deps
from backend.services.purchase_service import PurchaseService

router = APIRouter()

@router.post("/", response_model=schemas.purchase.Purchase)
def create_purchase(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    purchase_in: schemas.purchase.PurchaseCreate,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """
    Create a new purchase (bulk stock intake).
    This operation is atomic and creates inventory movements.
    """
    request_id = getattr(request.state, "request_id", "unknown")
    return PurchaseService.create_purchase(
        db=db,
        purchase_in=purchase_in,
        actor_id=current_user.id,
        request_id=request_id
    )

@router.get("/", response_model=List[schemas.purchase.Purchase])
def read_purchases(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_management),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve audit history of purchases.
    """
    return PurchaseService.list_purchases(db, skip=skip, limit=limit)

@router.get("/{id}", response_model=schemas.purchase.Purchase)
def read_purchase(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """
    Get purchase details by ID.
    """
    purchase = PurchaseService.get_purchase(db, purchase_id=id)
    if not purchase:
        raise HTTPException(status_code=404, detail="Purchase not found")
    return purchase
