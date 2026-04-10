from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.api import deps
from backend.core import security
from backend.core.config import settings
from backend.core.rate_limit import check_login_rate_limit

router = APIRouter()

@router.post("/login", response_model=schemas.user.Token, dependencies=[Depends(check_login_rate_limit)])
def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if not getattr(user, "is_active", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="La cuenta se encuentra desactivada. Contacte al superadmin.",
        )

    if deps.is_system_locked_for_user(db, user):
        raise HTTPException(
            status_code=status.HTTP_423_LOCKED,
            detail=deps.LOCKDOWN_MESSAGE,
        )

    if security.password_hash_needs_upgrade(user.password_hash):
        user.password_hash = security.get_password_hash(form_data.password)
        db.add(user)
        db.commit()

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )

    # Generate and save refresh token
    refresh_token = security.create_refresh_token()
    refresh_token_expires = datetime.now(timezone.utc) + timedelta(days=30)
    
    db_refresh_token = models.RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=refresh_token_expires
    )
    db.add(db_refresh_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.get("/me", response_model=schemas.user.User)
def read_user_me(
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.get("/status", response_model=schemas.admin.PublicSystemStatus)
def read_system_status(
    db: Session = Depends(deps.get_db),
) -> Any:
    setting = deps.get_system_setting(db)
    return {
        "lockdown_enabled": bool(setting.lockdown_enabled),
        "message": deps.LOCKDOWN_MESSAGE if setting.lockdown_enabled else "",
        "institutional_name": setting.institutional_name,
        "institutional_logo_url": setting.institutional_logo_url,
    }


@router.post("/refresh", response_model=schemas.user.Token)
def refresh_access_token(
    refresh_token: str,
    db: Session = Depends(deps.get_db),
) -> Any:
    """
    Refresh access token using a valid refresh token.
    """
    db_token = db.query(models.RefreshToken).filter(
        models.RefreshToken.token == refresh_token,
        models.RefreshToken.is_revoked == False,
        models.RefreshToken.expires_at > datetime.now(timezone.utc)
    ).first()
    
    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired refresh token",
        )
    
    user = db_token.user
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User not found or inactive",
        )

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        user.id, expires_delta=access_token_expires
    )
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }
