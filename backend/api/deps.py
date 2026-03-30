from typing import Generator
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session
from backend.core.config import settings
from backend.core import security
from backend.db.session import get_db
from backend import models, schemas

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.PROJECT_NAME.lower().replace(' ', '_')}/api/v1/login/access-token"
)

# Alternative URL if needed: "/api/v1/login/access-token"
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")

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
            status_code=status.HTTP_03_FORBIDDEN,
            detail="Could not validate credentials",
        )
    user = db.query(models.User).filter(models.User.id == int(token_data.sub)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

def get_current_active_user(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    # If there was an is_active field in your User model, check it here
    return current_user

def get_current_active_superadmin(
    current_user: models.User = Depends(get_current_user),
) -> models.User:
    if current_user.role != "superadmin":
        raise HTTPException(
            status_code=400, detail="The user doesn't have enough privileges"
        )
    return current_user
