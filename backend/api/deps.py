from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session
from backend.core.config import settings
from backend.core import security
from backend.db.runtime_schema import ensure_runtime_schema
from backend.db.session import get_db
from backend import models, schemas

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
LOCKDOWN_MESSAGE = "Sistema bloqueado. Contacte al desarrollador."


def get_system_setting(db: Session) -> models.SystemSetting:
    try:
        setting = db.query(models.SystemSetting).order_by(models.SystemSetting.id.asc()).first()
    except OperationalError:
        db.rollback()
        ensure_runtime_schema()
        setting = db.query(models.SystemSetting).order_by(models.SystemSetting.id.asc()).first()

    if setting:
        return setting

    setting = models.SystemSetting()
    db.add(setting)
    db.commit()
    db.refresh(setting)
    return setting


def is_system_locked_for_user(db: Session, user: models.User | None) -> bool:
    if user and user.role == "superadmin":
        return False
    return bool(get_system_setting(db).lockdown_enabled)

def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(reusable_oauth2)
) -> models.User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = schemas.user.TokenData(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(models.User).filter(models.User.id == int(token_data.sub)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not getattr(current_user, "is_active", True):
        raise HTTPException(
            status_code=403,
            detail="La cuenta se encuentra desactivada. Contacte al superadmin.",
        )

    if is_system_locked_for_user(db, current_user):
        raise HTTPException(
            status_code=423,
            detail=LOCKDOWN_MESSAGE,
        )

    return current_user

def get_current_active_superadmin(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if not getattr(current_user, "is_active", True):
        raise HTTPException(
            status_code=403,
            detail="La cuenta se encuentra desactivada. Contacte al superadmin.",
        )
    if current_user.role != "superadmin":
        raise HTTPException(
            status_code=403, detail="The user doesn't have enough privileges"
        )
    if is_system_locked_for_user(db, current_user):
        raise HTTPException(
            status_code=423,
            detail=LOCKDOWN_MESSAGE,
        )
    return current_user

def get_current_active_management(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    """Allows manager or superadmin roles."""
    if not getattr(current_user, "is_active", True):
        raise HTTPException(
            status_code=403,
            detail="La cuenta se encuentra desactivada. Contacte al superadmin.",
        )
    if current_user.role not in ("manager", "superadmin"):
        raise HTTPException(
            status_code=403, detail="Requires manager or superadmin role"
        )
    if is_system_locked_for_user(db, current_user):
        raise HTTPException(
            status_code=423,
            detail=LOCKDOWN_MESSAGE,
        )
    return current_user
