from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.building.Building])
def read_buildings(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve buildings assigned to current user.
    """
    if current_user.role == "superadmin":
        buildings = db.query(models.Building).offset(skip).limit(limit).all()
    else:
        buildings = db.query(models.Building).filter(models.Building.admin_id == current_user.id).all()
    return buildings

@router.get("/{id}/inventory", response_model=List[schemas.building.BuildingInventory])
def read_building_inventory(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get inventory for a specific building.
    IDOR check included.
    """
    if current_user.role != "superadmin":
        building = db.query(models.Building).filter(models.Building.id == id, models.Building.admin_id == current_user.id).first()
        if not building:
            raise HTTPException(status_code=403, detail="Not enough privileges to view this building's inventory")
    
    inventory = db.query(models.BuildingInventory).filter(models.BuildingInventory.building_id == id).all()
    return inventory
