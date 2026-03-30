from pydantic import BaseModel, ConfigDict
from typing import Optional

class ProductBase(BaseModel):
    sku: Optional[str] = None
    name: str
    categoria: Optional[str] = "General"
    description: Optional[str] = None
    unit: str
    precio: Optional[float] = 0.0
    imagen_url: Optional[str] = "/static/img/default-product.png"
    stock_actual: int = 0
    stock_minimo: int = 10
    is_active: bool = True

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    sku: Optional[str] = None
    name: Optional[str] = None
    categoria: Optional[str] = None
    description: Optional[str] = None
    unit: Optional[str] = None
    precio: Optional[float] = None
    stock_actual: Optional[int] = None
    stock_minimo: Optional[int] = None
    is_active: Optional[bool] = None

class Product(ProductBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
