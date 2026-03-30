from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime
from .product import Product

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
    created_at: datetime
    status: str
    items: List[OrderItem]
    model_config = ConfigDict(from_attributes=True)
