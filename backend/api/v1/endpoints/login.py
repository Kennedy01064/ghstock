from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Request
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
    request: Request,
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = db.query(models.User).filter(models.User.username == form_data.username).first()
    if not user or not security.verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS if False else status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    if security.password_hash_needs_upgrade(user.password_hash):
        user.password_hash = security.get_password_hash(form_data.password)
        db.add(user)
        db.commit()
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
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
