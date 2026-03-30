from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.product.Product])
def read_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve products (only active by default).
    """
    products = db.query(models.Product).filter(models.Product.is_active == True).offset(skip).limit(limit).all()
    return products

@router.get("/{id}", response_model=schemas.product.Product)
def read_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """
    Get product by ID.
    """
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=schemas.product.Product)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: schemas.product.ProductCreate,
    current_user: models.User = Depends(deps.get_current_active_superadmin),
) -> Any:
    """
    Create new product (Superadmin only).
    """
    product = models.Product(**product_in.model_dump())
    db.session.add(product)
    db.session.commit()
    db.session.refresh(product)
    return product
