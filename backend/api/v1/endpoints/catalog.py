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
    product = models.Product(**product_in.model_dump())
    db.add(product)
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
    for field, value in update_data.items():
        setattr(product, field, value)

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


@router.post("/import-csv")
async def import_csv(
    *,
    db: Session = Depends(deps.get_db),
    file: UploadFile = File(...),
    current_user: models.User = Depends(deps.get_current_active_management),
) -> Any:
    """Import products from a CSV file. Creates or updates products."""
    if not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="File must be a .csv")

    file_bytes = await file.read()
    try:
        decoded_text = file_bytes.decode("utf-8-sig")
    except UnicodeDecodeError:
        decoded_text = file_bytes.decode("cp1252", errors="replace")

    stream = io.StringIO(decoded_text)
    sample = stream.read(1024)
    stream.seek(0)
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=",;")
    except csv.Error:
        dialect = csv.excel

    reader = csv.DictReader(stream, dialect=dialect)
    created_count = 0
    updated_count = 0
    error_rows = []

    new_upload = models.CsvUpload(filename=file.filename)
    db.add(new_upload)
    db.flush()

    parsed_rows = []
    for row_num, row in enumerate(reader, start=2):
        try:
            sku = row.get("sku", "").strip()
            nombre = row.get("nombre", "").strip()
            unidad = row.get("unidad_medida", "").strip()
            precio_str = row.get("precio", "0").strip()
            descripcion = row.get("descripcion", "").strip()
            categoria = row.get("categoria", "General").strip()
            imagen_url = row.get("imagen_url", "").strip()
            stock_str = row.get("stock_actual", "0").strip()

            if not nombre:
                error_rows.append(f"Fila {row_num}: nombre vacío")
                continue

            precio = float(precio_str) if precio_str else 0.0
            stock = int(stock_str) if stock_str else 0

            parsed_rows.append(
                {
                    "sku": sku or None,
                    "name": nombre,
                    "unit": unidad,
                    "precio": precio,
                    "description": descripcion,
                    "categoria": categoria,
                    "imagen_url": imagen_url,
                    "stock_actual": stock,
                }
            )
        except Exception as e:
            error_rows.append(f"Fila {row_num}: {str(e)}")
            continue

    filters = []
    sku_values = {row["sku"] for row in parsed_rows if row["sku"]}
    name_values = {row["name"] for row in parsed_rows}
    if sku_values:
        filters.append(models.Product.sku.in_(sku_values))
    if name_values:
        filters.append(models.Product.name.in_(name_values))

    existing_products = db.query(models.Product).filter(or_(*filters)).all() if filters else []
    existing_by_sku = {product.sku: product for product in existing_products if product.sku}
    existing_by_name = {product.name: product for product in existing_products}
    pending_inserts_by_sku = {}
    pending_inserts_by_name = {}
    update_mappings = {}
    insert_mappings = []

    for row in parsed_rows:
        product = None
        if row["sku"]:
            product = existing_by_sku.get(row["sku"]) or pending_inserts_by_sku.get(row["sku"])
        if not product:
            product = existing_by_name.get(row["name"]) or pending_inserts_by_name.get(row["name"])

        if isinstance(product, dict):
            updated_count += 1
            if row["sku"]:
                product["sku"] = row["sku"]
                pending_inserts_by_sku[row["sku"]] = product
            product["name"] = row["name"]
            if row["unit"]:
                product["unit"] = row["unit"]
            product["precio"] = row["precio"]
            if row["description"]:
                product["description"] = row["description"]
            if row["categoria"]:
                product["categoria"] = row["categoria"]
            if row["imagen_url"]:
                product["imagen_url"] = row["imagen_url"]
            if row["stock_actual"] > 0:
                product["stock_actual"] = row["stock_actual"]
            pending_inserts_by_name[row["name"]] = product
            continue

        if product:
            updated_count += 1
            mapping = update_mappings.get(product.id)
            if not mapping:
                mapping = {"id": product.id}
                update_mappings[product.id] = mapping

            if row["sku"]:
                mapping["sku"] = row["sku"]
                existing_by_sku[row["sku"]] = product
            mapping["name"] = row["name"]
            existing_by_name[row["name"]] = product
            if row["unit"]:
                mapping["unit"] = row["unit"]
            mapping["precio"] = row["precio"]
            if row["description"]:
                mapping["description"] = row["description"]
            if row["categoria"]:
                mapping["categoria"] = row["categoria"]
            if row["imagen_url"]:
                mapping["imagen_url"] = row["imagen_url"]
            if row["stock_actual"] > 0:
                mapping["stock_actual"] = row["stock_actual"]
            continue

        insert_mapping = {
            "sku": row["sku"],
            "name": row["name"],
            "unit": row["unit"] or "Unidad",
            "categoria": row["categoria"] or "General",
            "precio": row["precio"],
            "description": row["description"] or None,
            "imagen_url": row["imagen_url"] or "/static/img/default-product.png",
            "stock_actual": row["stock_actual"],
            "stock_minimo": 10,
            "is_active": True,
            "source_csv_id": new_upload.id,
            "is_dynamic": False,
        }
        insert_mappings.append(insert_mapping)
        created_count += 1
        if row["sku"]:
            pending_inserts_by_sku[row["sku"]] = insert_mapping
        pending_inserts_by_name[row["name"]] = insert_mapping

    if insert_mappings:
        db.bulk_insert_mappings(models.Product, insert_mappings)
    if update_mappings:
        db.bulk_update_mappings(models.Product, list(update_mappings.values()))

    new_upload.products_created = created_count
    new_upload.products_updated = updated_count
    db.commit()

    return {
        "id": new_upload.id,
        "filename": new_upload.filename,
        "products_created": created_count,
        "products_updated": updated_count,
        "errors": error_rows[:10],
    }


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
