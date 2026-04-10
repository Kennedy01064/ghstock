from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session, selectinload

from backend import models, schemas
from backend.api import deps
from backend.core.security import get_password_hash

router = APIRouter()


def _client_ip(request: Request | None) -> str | None:
    if request is None or request.client is None:
        return None
    return request.client.host


def _log_user_audit(
    db: Session,
    *,
    actor: models.User,
    action: str,
    resource_id: int | str | None,
    details: str,
    request: Request | None = None,
) -> None:
    db.add(
        models.AuditLog(
            user_id=actor.id,
            action=action,
            resource_type="user",
            resource_id=str(resource_id) if resource_id is not None else None,
            details=details,
            ip_address=_client_ip(request),
        )
    )
    db.commit()


@router.get("/", response_model=List[schemas.user.UserWithBuildings])
def list_users(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_management),
    role: Optional[str] = None,
    include_inactive: bool = False,
) -> Any:
    """List users for administration or building assignment flows."""
    query = db.query(models.User).options(
        selectinload(models.User.assigned_buildings)
    )

    if current_user.role == "superadmin":
        valid_roles = {"admin", "manager", "superadmin"}
        if role in valid_roles:
            query = query.filter(models.User.role == role)
        else:
            query = query.filter(models.User.role.in_(sorted(valid_roles)))
    else:
        query = query.filter(models.User.role == "admin")
        if role and role != "admin":
            raise HTTPException(status_code=403, detail="Managers can only list admin users")

    if not include_inactive:
        query = query.filter(models.User.is_active == True)

    return query.order_by(models.User.name.asc(), models.User.username.asc()).all()


@router.get("/{id}", response_model=schemas.user.UserWithBuildings)
def get_user(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Get a single user."""
    user = db.query(models.User).options(
        selectinload(models.User.assigned_buildings)
    ).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if current_user.role != "superadmin" and user.role != "admin":
        raise HTTPException(status_code=403, detail="Managers can only inspect admin users")

    return user


@router.post("/", response_model=schemas.user.User)
def create_user(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    user_in: schemas.user.UserCreate,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Create a new user with role constraints based on the acting account."""
    allowed_roles = {"admin", "manager"} if current_user.role == "superadmin" else {"admin"}
    if user_in.role not in allowed_roles:
        if current_user.role == "manager":
            raise HTTPException(status_code=403, detail="Managers can only create admin accounts")
        raise HTTPException(status_code=400, detail="Role must be 'admin' or 'manager'")
    if len(user_in.password) < 6:
        raise HTTPException(status_code=400, detail="Password must be at least 6 characters")

    existing = db.query(models.User).filter(models.User.username == user_in.username).first()
    if existing:
        raise HTTPException(status_code=409, detail=f"Username '{user_in.username}' already exists")

    user = models.User(
        username=user_in.username,
        name=user_in.name,
        role=user_in.role,
        is_active=user_in.is_active,
        password_hash=get_password_hash(user_in.password),
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    _log_user_audit(
        db,
        actor=current_user,
        action="user.created",
        resource_id=user.id,
        details=f"Created {user.role} account @{user.username} (active={user.is_active}).",
        request=request,
    )
    return user


@router.put("/{id}", response_model=schemas.user.UserWithBuildings)
def update_user(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    id: int,
    user_in: schemas.user.UserUpdate,
    building_ids: List[int] = Query(None),
    clear_buildings: bool = Query(False),
    current_user: models.User = Depends(deps.get_current_active_superadmin),
) -> Any:
    """Update a user and optionally re-assign buildings."""
    user = db.query(models.User).options(
        selectinload(models.User.assigned_buildings)
    ).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role == "superadmin":
        raise HTTPException(status_code=403, detail="Cannot edit superadmin accounts")

    changed_fields: list[str] = []

    if user_in.username is not None and user_in.username != user.username:
        conflict = db.query(models.User).filter(
            models.User.username == user_in.username,
            models.User.id != id,
        ).first()
        if conflict:
            raise HTTPException(status_code=409, detail=f"Username '{user_in.username}' already taken")
        user.username = user_in.username
        changed_fields.append("username")

    if user_in.name is not None and user_in.name != user.name:
        user.name = user_in.name
        changed_fields.append("name")

    if user_in.role is not None:
        if user_in.role not in ("admin", "manager"):
            raise HTTPException(status_code=400, detail="Role must be 'admin' or 'manager'")
        if user_in.role != user.role:
            user.role = user_in.role
            changed_fields.append("role")

    if user_in.password:
        if len(user_in.password) < 6:
            raise HTTPException(status_code=400, detail="Password must be at least 6 characters")
        user.password_hash = get_password_hash(user_in.password)
        changed_fields.append("password")

    if user_in.is_active is not None and user_in.is_active != user.is_active:
        user.is_active = user_in.is_active
        changed_fields.append("is_active")

    if clear_buildings or building_ids is not None:
        for building in user.assigned_buildings:
            building.admin_id = None

        for building_id in building_ids or []:
            building = db.query(models.Building).filter(models.Building.id == building_id).first()
            if building:
                building.admin_id = user.id

        changed_fields.append("assigned_buildings")

    db.commit()
    db.refresh(user)

    details = ", ".join(changed_fields) if changed_fields else "no field changes"
    _log_user_audit(
        db,
        actor=current_user,
        action="user.updated",
        resource_id=user.id,
        details=f"Updated @{user.username}: {details}.",
        request=request,
    )
    return user


@router.patch("/{id}/toggle-active", response_model=schemas.user.UserWithBuildings)
def toggle_user_active(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superadmin),
) -> Any:
    """Toggle an admin or manager account between active and inactive."""
    user = db.query(models.User).options(
        selectinload(models.User.assigned_buildings)
    ).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role == "superadmin":
        raise HTTPException(status_code=403, detail="Cannot suspend superadmin accounts")
    if user.id == current_user.id:
        raise HTTPException(status_code=403, detail="Cannot suspend your own account")

    user.is_active = not bool(user.is_active)
    db.commit()
    db.refresh(user)

    _log_user_audit(
        db,
        actor=current_user,
        action="user.toggled_active",
        resource_id=user.id,
        details=f"Set @{user.username} active={user.is_active}.",
        request=request,
    )
    return user


@router.delete("/{id}")
def delete_user(
    *,
    request: Request,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_superadmin),
) -> Any:
    """Delete an admin or manager user (detaches their buildings)."""
    user = db.query(models.User).options(
        selectinload(models.User.assigned_buildings)
    ).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role == "superadmin":
        raise HTTPException(status_code=403, detail="Cannot delete superadmin accounts")
    if user.id == current_user.id:
        raise HTTPException(status_code=403, detail="Cannot delete your own account")

    deleted_username = user.username
    deleted_role = user.role

    for building in user.assigned_buildings:
        building.admin_id = None

    db.delete(user)
    db.commit()

    _log_user_audit(
        db,
        actor=current_user,
        action="user.deleted",
        resource_id=id,
        details=f"Deleted {deleted_role} account @{deleted_username}.",
        request=request,
    )
    return {"message": f"User '{deleted_username}' deleted"}
