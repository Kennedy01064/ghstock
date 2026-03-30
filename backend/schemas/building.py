from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from .product import Product

class BuildingBase(BaseModel):
    name: str
    address: Optional[str] = None
    departments_count: int = 0
    imagen_frontis: Optional[str] = None

class BuildingCreate(BuildingBase):
    admin_id: Optional[int] = None

class Building(BuildingBase):
    id: int
    admin_id: Optional[int] = None
    model_config = ConfigDict(from_attributes=True)

class BuildingInventory(BaseModel):
    id: int
    building_id: int
    product_id: int
    quantity: int
    last_updated: datetime
    product: Product
    model_config = ConfigDict(from_attributes=True)
