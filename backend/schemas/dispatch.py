from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime, date
from .user import User
from .product import Product
from .order import OrderDetail


class DispatchBatchItemDetail(BaseModel):
    id: int
    product_id: int
    total_quantity: int
    product: Product
    model_config = ConfigDict(from_attributes=True)


class DispatchBatchSummary(BaseModel):
    id: int
    created_by_id: int
    created_at: datetime
    status: str
    model_config = ConfigDict(from_attributes=True)


class DispatchBatchDetail(BaseModel):
    id: int
    created_by: Optional[User] = None
    created_at: datetime
    status: str
    orders: List[OrderDetail]
    items: List[DispatchBatchItemDetail]
    model_config = ConfigDict(from_attributes=True)


class PurchaseItemCreate(BaseModel):
    product_id: int
    quantity: int
    unit_price: float = 0.0


class PurchaseCreate(BaseModel):
    supplier: Optional[str] = None
    invoice_number: Optional[str] = None
    purchase_date: date
    notes: Optional[str] = None
    items: List[PurchaseItemCreate]


class PurchaseItemDetail(BaseModel):
    id: int
    product_id: int
    quantity: int
    unit_price: float
    product: Product
    model_config = ConfigDict(from_attributes=True)


class PurchaseDetail(BaseModel):
    id: int
    supplier: Optional[str] = None
    invoice_number: Optional[str] = None
    purchase_date: date
    total_amount: Optional[float] = 0.0
    notes: Optional[str] = None
    created_by_id: int
    created_at: datetime
    created_by: Optional[User] = None
    items: List[PurchaseItemDetail]
    model_config = ConfigDict(from_attributes=True)


class PurchaseSummary(BaseModel):
    id: int
    supplier: Optional[str] = None
    invoice_number: Optional[str] = None
    purchase_date: date
    total_amount: Optional[float] = 0.0
    created_by_id: int
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class DispatchHistoryResponse(BaseModel):
    batches: List[DispatchBatchDetail]
    orders: List[OrderDetail]
