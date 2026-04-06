from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, selectinload
from backend import models, schemas
from backend.api import deps
from backend.core.security import get_password_hash

router = APIRouter()


@router.get("/", response_model=List[schemas.user.UserWithBuildings])
def list_users(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_management),
    role: Optional[str] = None,
) -> Any:
    """List all admin and manager users."""
    query = db.query(models.User).options(
        selectinload(models.User.assigned_buildings)
    ).filter(models.User.role.in_(["admin", "manager"]))
    if role in {"admin", "manager"}:
        query = query.filter(models.User.role == role)
    users = query.order_by(models.User.name.asc(), models.User.username.asc()).all()
    return users


@router.get("/{id}", response_model=schemas.user.UserWithBuildings)
def get_user(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Get a single admin or manager user."""
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role not in ("admin", "manager", "superadmin"):
        raise HTTPException(status_code=400, detail="Unsupported user role")
    return user


@router.post("/", response_model=schemas.user.User)
def create_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Create a new admin or manager user."""
    if user_in.role not in ("admin", "manager"):
        raise HTTPException(status_code=400, detail="Role must be 'admin' or 'manager'")
    if current_user.role != "superadmin" and user_in.role != "admin":
        raise HTTPException(status_code=403, detail="Only superadmin can create manager users")
    if len(user_in.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    existing = db.query(models.User).filter(models.User.username == user_in.username).first()
    if existing:
        raise HTTPException(status_code=400, detail=f"Username '{user_in.username}' already exists")

    user = models.User(
        username=user_in.username,
        name=user_in.name,
        role=user_in.role,
        password_hash=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.put("/{id}", response_model=schemas.user.UserWithBuildings)
def update_user(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    user_in: schemas.user.UserUpdate,
    building_ids: List[int] = Query(None),
    clear_buildings: bool = Query(False),
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Update a user and optionally re-assign buildings."""
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.username == "krojas" or user.role == "superadmin":
        raise HTTPException(status_code=403, detail="Cannot edit superadmin accounts")
    if user.role == "manager" and current_user.role != "superadmin" and current_user.id != id:
        raise HTTPException(status_code=403, detail="Only superadmin can edit other managers")

    if user_in.username is not None:
        conflict = db.query(models.User).filter(
            models.User.username == user_in.username,
            models.User.id != id
        ).first()
        if conflict:
            raise HTTPException(status_code=400, detail=f"Username '{user_in.username}' already taken")
        user.username = user_in.username

    if user_in.name is not None:
        user.name = user_in.name

    if user_in.role is not None:
        if user_in.role not in ("admin", "manager"):
            raise HTTPException(status_code=400, detail="Role must be 'admin' or 'manager'")
        if user_in.role != user.role:
            if current_user.role != "superadmin":
                raise HTTPException(status_code=403, detail="Only superadmin can change user roles")
            user.role = user_in.role

    if user_in.password:
        if len(user_in.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        user.password_hash = get_password_hash(user_in.password)

    if clear_buildings or building_ids is not None:
        # Clear old assignments
        for b in user.assigned_buildings:
            b.admin_id = None
        # Apply new ones
        for b_id in building_ids or []:
            bldg = db.query(models.Building).filter(models.Building.id == b_id).first()
            if bldg:
                bldg.admin_id = user.id

    db.commit()
    db.refresh(user)
    return user


@router.delete("/{id}")
def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Delete an admin or manager user (detaches their buildings)."""
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.username == "krojas" or user.role == "superadmin":
        raise HTTPException(status_code=403, detail="Cannot delete superadmin accounts")
    if user.role == "manager" and current_user.role != "superadmin":
        raise HTTPException(status_code=403, detail="Only superadmin can delete manager accounts")

    for b in user.assigned_buildings:
        b.admin_id = None

    db.delete(user)
    db.commit()
    return {"message": f"User '{user.username}' deleted"}
