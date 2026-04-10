from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from .product import Product
from .user import User
from .building import Building

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItem(OrderItemBase):
    id: int
    order_id: int
    nombre_producto_snapshot: Optional[str] = None
    precio_unitario: Optional[float] = 0.0
    product: Product
    model_config = ConfigDict(from_attributes=True)

class OrderBase(BaseModel):
    building_id: int

class OrderCreate(OrderBase):
    pass

class Order(OrderBase):
    id: int
    created_by_id: int
    status: str
    items: List[OrderItem]
    model_config = ConfigDict(from_attributes=True)

class OrderDetail(Order):
    building: Building
    created_by: Optional[User] = None
    rejection_note: Optional[str] = None

class OrderItemUpdate(BaseModel):
    quantity: int

class ConsumptionReportRow(BaseModel):
    building_name: str
    product_name: str
    unit: str
    imagen_url: Optional[str] = None
    total_consumed: int
    events: int
    last_reported: Optional[datetime] = None
