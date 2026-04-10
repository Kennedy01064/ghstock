from pydantic import BaseModel, ConfigDict
from typing import Optional, List

class UserBase(BaseModel):
    username: str
    name: Optional[str] = None
    role: str = "admin"
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    name: Optional[str] = None
    password: Optional[str] = None
    role: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class UserWithBuildings(User):
    assigned_buildings: List["BuildingSimple"] = []

class BuildingSimple(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)

UserWithBuildings.model_rebuild()

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    sub: Optional[str] = None

