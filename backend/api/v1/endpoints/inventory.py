from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.api import deps
from backend.services.building_inventory_service import BuildingInventoryService
from backend.domain.errors import DomainError

router = APIRouter()

def _assert_building_access(building_id: int, current_user: models.User):
    if current_user.role in ("superadmin", "manager"):
        return
    my_building_ids = {b.id for b in current_user.assigned_buildings}
    if building_id not in my_building_ids:
        raise HTTPException(status_code=403, detail=f"No access to building {building_id}")
@router.get("/", response_model=List[schemas.inventory.BuildingInventoryItem])
def list_inventory(
    *,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
    building_id: int | None = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
    response: Response,
) -> Any:
    """List building inventory items visible to the current user."""
    query = db.query(models.BuildingInventory)
    if current_user.role in ("superadmin", "manager"):
        if building_id:
            query = query.filter(models.BuildingInventory.building_id == building_id)
    else:
        my_building_ids = [b.id for b in current_user.assigned_buildings]
        if building_id:
            if building_id not in my_building_ids:
                raise HTTPException(status_code=403, detail="No access to requested building")
            query = query.filter(models.BuildingInventory.building_id == building_id)
        else:
            query = query.filter(models.BuildingInventory.building_id.in_(my_building_ids))

    total = query.count()
    response.headers["X-Total-Count"] = str(total)
    return query.order_by(models.BuildingInventory.last_updated.desc()).offset(skip).limit(limit).all()


@router.post("/transfer")
def transfer_inventory(
    *,
    db: Session = Depends(deps.get_db),
    transfer_in: schemas.inventory.TransferInventoryRequest,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Transfer stock from one building to another."""
    _assert_building_access(transfer_in.from_building_id, current_user)
    # Target building might not be owned by the same person, but superadmin/manager can do it.
    # If not admin, they can only transfer to buildings they also manage? 
    # Let's be strict for now: must have access to both if not superadmin.
    _assert_building_access(transfer_in.to_building_id, current_user)

    try:
        BuildingInventoryService.transfer_stock(
            db=db,
            from_building_id=transfer_in.from_building_id,
            to_building_id=transfer_in.to_building_id,
            product_id=transfer_in.product_id,
            quantity=transfer_in.quantity,
            actor_id=current_user.id
        )
        db.commit()
        return {"message": "Transfer successful"}
    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/return")
def return_to_central(
    *,
    db: Session = Depends(deps.get_db),
    return_in: schemas.inventory.ReturnInventoryRequest,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Return stock from building to central warehouse."""
    _assert_building_access(return_in.building_id, current_user)

    try:
        BuildingInventoryService.return_stock(
            db=db,
            building_id=return_in.building_id,
            product_id=return_in.product_id,
            quantity=return_in.quantity,
            actor_id=current_user.id,
            reason=return_in.reason
        )
        db.commit()
        return {"message": "Return to central successful"}
    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/shrinkage")
def register_shrinkage(
    *,
    db: Session = Depends(deps.get_db),
    shrink_in: schemas.inventory.ShrinkageRequest,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Register stock loss/shrinkage in a building."""
    _assert_building_access(shrink_in.building_id, current_user)

    try:
        BuildingInventoryService.register_shrinkage(
            db=db,
            building_id=shrink_in.building_id,
            product_id=shrink_in.product_id,
            quantity=shrink_in.quantity,
            actor_id=current_user.id,
            reason=shrink_in.reason
        )
        db.commit()
        return {"message": "Shrinkage registered successfully"}
    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/history", response_model=List[schemas.inventory.InventoryMovement])
def get_movement_history(
    *,
    db: Session = Depends(deps.get_db),
    building_id: Optional[int] = None,
    product_id: Optional[int] = None,
    movement_type: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, le=500),
    month: Optional[int] = Query(None, ge=1, le=12),
    year: Optional[int] = Query(None, ge=2020),
    current_user: models.User = Depends(deps.get_current_active_user),
    response: Response,
) -> Any:
    """Get inventory movement history with filtering."""
    
    # Define query to get total count
    query = db.query(models.InventoryMovement)
    
    if current_user.role not in ("superadmin", "manager"):
        # Non-privileged role: strict scope to assigned buildings only.
        my_building_ids = [b.id for b in current_user.assigned_buildings]
        if building_id is not None:
            if building_id not in my_building_ids:
                raise HTTPException(status_code=403, detail=f"No access to building {building_id}")
            query = query.filter(models.InventoryMovement.building_id == building_id)
        else:
            if not my_building_ids:
                response.headers["X-Total-Count"] = "0"
                return []
            query = query.filter(models.InventoryMovement.building_id.in_(my_building_ids))
    else:
        # superadmin / manager
        if building_id:
            query = query.filter(models.InventoryMovement.building_id == building_id)

    if product_id:
        query = query.filter(models.InventoryMovement.product_id == product_id)
    if movement_type:
        query = query.filter(models.InventoryMovement.movement_type == movement_type)
    
    if year:
        query = query.filter(func.extract('year', models.InventoryMovement.created_at) == year)
    if month:
        query = query.filter(func.extract('month', models.InventoryMovement.created_at) == month)

    total = query.count()
    response.headers["X-Total-Count"] = str(total)
    
    return query.order_by(models.InventoryMovement.created_at.desc()).offset(skip).limit(limit).all()


@router.get("/{id}", response_model=schemas.inventory.BuildingInventoryItem)
def get_inventory_item(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Get a single building inventory item."""
    inv = db.query(models.BuildingInventory).filter(models.BuildingInventory.id == id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    _assert_building_access(inv.building_id, current_user)
    return inv


@router.post("/", response_model=schemas.inventory.BuildingInventoryItem)
def add_inventory_item(
    *,
    db: Session = Depends(deps.get_db),
    inv_in: schemas.inventory.AddInventoryRequest,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Add a product to a building's local inventory."""
    _assert_building_access(inv_in.building_id, current_user)

    if inv_in.quantity < 1:
        raise HTTPException(status_code=400, detail="Quantity must be at least 1")

    try:
        BuildingInventoryService.receive_stock(
            db=db,
            building_id=inv_in.building_id,
            product_id=inv_in.product_id,
            quantity=inv_in.quantity,
            actor_id=current_user.id,
            reference_id=inv_in.building_id,
            reference_type='manual_add'
        )
        db.commit()
    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
    # Return the updated item
    updated = db.query(models.BuildingInventory).filter_by(
        building_id=inv_in.building_id,
        product_id=inv_in.product_id
    ).first()
    return updated


@router.post("/{id}/consume", response_model=schemas.inventory.BuildingInventoryItem)
def consume_inventory(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    consume_in: schemas.inventory.ConsumeInventoryRequest,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Report consumption of a building inventory item."""
    inv = db.query(models.BuildingInventory).filter(models.BuildingInventory.id == id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    _assert_building_access(inv.building_id, current_user)

    try:
        BuildingInventoryService.consume_stock(
            db=db,
            building_id=inv.building_id,
            product_id=inv.product_id,
            quantity=consume_in.quantity,
            actor_id=current_user.id
        )
        db.commit()
        db.refresh(inv)
        return inv
    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/{id}/adjust", response_model=schemas.inventory.BuildingInventoryItem)
def adjust_inventory(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    adjust_in: schemas.inventory.AdjustInventoryRequest,
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """Manually set the quantity of a building inventory item."""
    inv = db.query(models.BuildingInventory).filter(models.BuildingInventory.id == id).first()
    if not inv:
        raise HTTPException(status_code=404, detail="Inventory item not found")
    _assert_building_access(inv.building_id, current_user)

    try:
        BuildingInventoryService.adjust_stock(
            db=db,
            building_id=inv.building_id,
            product_id=inv.product_id,
            new_quantity=adjust_in.quantity,
            actor_id=current_user.id,
            reason=adjust_in.note or "Manual Adjustment"
        )
        db.commit()
        db.refresh(inv)
        return inv
    except DomainError as e:
        raise HTTPException(status_code=400, detail=str(e))
