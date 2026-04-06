from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import date, datetime
from .product import Product

class PurchaseItemBase(BaseModel):
    product_id: int
    quantity: int = Field(..., gt=0)
    unit_price: Optional[float] = Field(0.0, ge=0.0)

class PurchaseItemCreate(PurchaseItemBase):
    pass

class PurchaseItem(PurchaseItemBase):
    id: int
    purchase_id: int
    product: Optional[Product] = None
    
    model_config = ConfigDict(from_attributes=True)

class PurchaseBase(BaseModel):
    supplier: Optional[str] = None
    invoice_number: Optional[str] = None
    purchase_date: date
    total_amount: Optional[float] = 0.0
    notes: Optional[str] = None

class PurchaseCreate(PurchaseBase):
    items: List[PurchaseItemCreate]

class PurchaseUpdate(BaseModel):
    supplier: Optional[str] = None
    invoice_number: Optional[str] = None
    purchase_date: Optional[date] = None
    total_amount: Optional[float] = None
    notes: Optional[str] = None

class Purchase(PurchaseBase):
    id: int
    created_by_id: int
    created_at: datetime
    items: List[PurchaseItem]
    
    model_config = ConfigDict(from_attributes=True)
