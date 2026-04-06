from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from .building import Building
from .product import Product


class BuildingInventoryItem(BaseModel):
    id: int
    building_id: int
    product_id: int
    quantity: int
    last_updated: datetime
    product: Product
    building: Optional[Building] = None
    model_config = ConfigDict(from_attributes=True)


class AddInventoryRequest(BaseModel):
    building_id: int
    product_id: int
    quantity: int = 1


class ConsumeInventoryRequest(BaseModel):
    quantity: int


class AdjustInventoryRequest(BaseModel):
    quantity: int
    note: Optional[str] = None


class TransferInventoryRequest(BaseModel):
    from_building_id: int
    to_building_id: int
    product_id: int
    quantity: int


class ReturnInventoryRequest(BaseModel):
    building_id: int
    product_id: int
    quantity: int
    reason: Optional[str] = "Return to central"


class ShrinkageRequest(BaseModel):
    building_id: int
    product_id: int
    quantity: int
    reason: str


class InventoryMovement(BaseModel):
    id: int
    product_id: int
    quantity: int
    movement_type: str
    building_id: Optional[int] = None
    reference_id: Optional[int] = None
    reference_type: Optional[str] = None
    created_at: datetime
    created_by_id: int
    
    product: Product
    model_config = ConfigDict(from_attributes=True)
