import csv
import io
from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy import or_
from sqlalchemy.orm import Session
from datetime import datetime, timezone

from backend import models, schemas
from backend.api import deps
from backend.services.scraper import ScraperService
from backend.services.inventory_service import InventoryService
from backend.services.catalog_import_service import CatalogImportService

router = APIRouter()


@router.get("/", response_model=List[schemas.product.Product])
def read_products(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """Retrieve active products."""
    products = db.query(models.Product).filter(models.Product.is_active == True).offset(skip).limit(limit).all()
    return products


@router.get("/all", response_model=List[schemas.product.Product])
def read_all_products(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_management),
    skip: int = 0,
    limit: int = 50,
    q: str = None,
) -> Any:
    """Retrieve all products including inactive (management only)."""
    query = db.query(models.Product)
    if q:
        query = query.filter(
            (models.Product.name.ilike(f"%{q}%")) | 
            (models.Product.sku.ilike(f"%{q}%"))
        )
    products = query.order_by(models.Product.name).offset(skip).limit(limit).all()
    return products


@router.get("/uploads", response_model=List[schemas.csv_upload.CsvUpload])
def read_csv_uploads(
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_management),
    limit: int = 20,
) -> Any:
    """Retrieve recent CSV upload batches."""
    return (
        db.query(models.CsvUpload)
        .order_by(models.CsvUpload.uploaded_at.desc())
        .limit(limit)
        .all()
    )


@router.get("/{id}", response_model=schemas.product.Product)
def read_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> Any:
    """Get product by ID."""
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("/", response_model=schemas.product.Product)
def create_product(
    *,
    db: Session = Depends(deps.get_db),
    product_in: schemas.product.ProductCreate,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Create new product."""
    initial_stock = product_in.stock_actual
    product_data = product_in.model_dump()
    product_data['stock_actual'] = 0
    product = models.Product(**product_data)
    db.add(product)
    db.flush()
    if initial_stock > 0:
        InventoryService.adjust_stock(db=db, product_id=product.id, new_quantity=initial_stock, actor_id=current_user.id, reason='Initial Creation')
    db.commit()
    db.refresh(product)
    return product


@router.put("/{id}", response_model=schemas.product.Product)
def update_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    product_in: schemas.product.ProductUpdate,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Update product details."""
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_in.model_dump(exclude_unset=True)
    new_stock = update_data.pop('stock_actual', None)
    for field, value in update_data.items():
        setattr(product, field, value)
    db.flush()
    if new_stock is not None and new_stock != product.stock_actual:
        InventoryService.adjust_stock(db=db, product_id=product.id, new_quantity=new_stock, actor_id=current_user.id, reason='Manual Update')
    db.commit()
    db.refresh(product)
    return product


@router.patch("/{id}/toggle", response_model=schemas.product.Product)
def toggle_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Toggle product active/inactive status."""
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.is_active = not product.is_active
    db.commit()
    db.refresh(product)
    return product


@router.post("/import-preview", response_model=schemas.catalog_import.ImportPreview)
async def import_preview(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """
    Step 1: Upload CSV and get a preview of proposed changes.
    Does NOT modify the database.
    """
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a .csv")

    file_bytes = await file.read()
    try:
        decoded_text = file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        decoded_text = file_bytes.decode("cp1252", errors="replace")

    rows = CatalogImportService.parse_csv(decoded_text)
    preview = CatalogImportService.preview_import(
        db=db,
        rows=rows,
        filename=file.filename
    )
    return preview


@router.post("/import-commit")
def import_commit(
    *,
    db: Session = Depends(deps.get_db),
    commit_data: schemas.catalog_import.ImportCommitRequest,
    preview_rows: List[schemas.catalog_import.ImportPreviewRow],
    filename: str,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """
    Step 2: Apply the previewed changes to the database.
    """
    return CatalogImportService.commit_import(
        db=db,
        preview_rows=preview_rows,
        update_stock=commit_data.update_stock,
        actor_id=current_user.id,
        filename=filename
    )


@router.post("/import-csv")
async def import_csv_legacy(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """
    Legacy import (Direct write). 
    Maintained for backward compatibility but calls the new service logic.
    """
    file_bytes = await file.read()
    try:
        decoded_text = file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        decoded_text = file_bytes.decode("cp1252", errors="replace")

    rows = CatalogImportService.parse_csv(decoded_text)
    preview = CatalogImportService.preview_import(db, rows, file.filename)
    
    return CatalogImportService.commit_import(
        db=db,
        preview_rows=preview.preview_rows,
        update_stock=True,
        actor_id=current_user.id,
        filename=file.filename
    )


@router.delete("/uploads/{id}")
def delete_csv_upload(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Delete a CSV upload batch. Products with history are soft-deleted."""
    upload = db.query(models.CsvUpload).filter(models.CsvUpload.id == id).first()
    if not upload:
        raise HTTPException(status_code=404, detail="Upload not found")

    products = db.query(models.Product).filter(models.Product.source_csv_id == id).all()
    deleted_count = 0
    soft_deleted_count = 0

    for p in products:
        has_orders = db.query(models.OrderItem).filter(models.OrderItem.product_id == p.id).first()
        has_movements = db.query(models.InventoryMovement).filter(models.InventoryMovement.product_id == p.id).first()
        if has_orders or has_movements:
            p.is_active = False
            soft_deleted_count += 1
        else:
            db.delete(p)
            deleted_count += 1

    db.delete(upload)
    db.commit()
    return {
        "message": f"Batch deleted. {deleted_count} hard-deleted, {soft_deleted_count} soft-deleted."
    }


@router.post("/preview", response_model=Any)
async def preview_product(
    *,
    url: str,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Scrape product details for preview."""
    details = await ScraperService.get_product_details(url)
    if "error" in details:
        raise HTTPException(status_code=400, detail=details["error"])
    return details


@router.put("/{id}/sync", response_model=schemas.product.Product)
async def sync_product(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Sync existing product with its source URL."""
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    if not product.source_url:
        raise HTTPException(status_code=400, detail="Product has no source URL")

    details = await ScraperService.get_product_details(product.source_url)
    if "error" in details:
        raise HTTPException(status_code=400, detail=details["error"])

    product.name = details.get("name", product.name)
    product.precio = details.get("price", product.precio)
    product.description = details.get("description", product.description)
    product.imagen_url = details.get("image_url", product.imagen_url)
    product.last_synced_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(product)
    return product
