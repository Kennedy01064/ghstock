from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.api import deps
from backend.services.building_inventory_service import BuildingInventoryService
from backend.domain.errors import DomainConflictError, DomainValidationError

router = APIRouter()

@router.post("/", response_model=Any)
def transfer_stock(
    *,
    db: Session = Depends(deps.get_db),
    transfer_in: schemas.transfer.StockTransferCreate,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """
    Directly move stock from one building to another.
    Only available for Managers/Superadmins.
    """
    try:
        service = BuildingInventoryService()
        source_inv, target_inv = service.transfer_stock(
            db=db,
            from_building_id=transfer_in.from_building_id,
            to_building_id=transfer_in.to_building_id,
            product_id=transfer_in.product_id,
            quantity=transfer_in.quantity,
            actor_id=current_user.id
        )
        
        # Explicitly record the transfer
        db_transfer = models.StockTransfer(
            from_building_id=transfer_in.from_building_id,
            to_building_id=transfer_in.to_building_id,
            product_id=transfer_in.product_id,
            quantity=transfer_in.quantity,
            actor_id=current_user.id
        )
        db.add(db_transfer)
        
        db.commit()
        return {
            "message": "Transfer successful",
            "from_building": source_inv.building_id,
            "to_building": target_inv.building_id,
            "product_id": transfer_in.product_id,
            "new_source_quantity": source_inv.quantity,
            "new_target_quantity": target_inv.quantity
        }
    except (DomainConflictError, DomainValidationError) as e:
        raise HTTPException(status_code=400, detail=str(e))
