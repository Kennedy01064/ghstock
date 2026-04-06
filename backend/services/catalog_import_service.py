import csv
import io
import uuid
from typing import List, Dict, Any, Tuple
from sqlalchemy.orm import Session
from sqlalchemy import or_

from backend import models, schemas
from backend.services.inventory_service import InventoryService
from backend.domain.errors import DomainValidationError

class CatalogImportService:
    @staticmethod
    def parse_csv(file_content: str) -> List[Dict[str, Any]]:
        """
        Parse CSV content and return a list of dictionaries.
        """
        stream = io.StringIO(file_content)
        try:
            # Sniff for delimiter
            sample = stream.read(1024)
            stream.seek(0)
            dialect = csv.Sniffer().sniff(sample, delimiters=",;")
        except Exception:
            dialect = csv.excel

        reader = csv.DictReader(stream, dialect=dialect)
        rows = []
        for row in reader:
            # Normalize keys to lowercase and strip
            normalized_row = {k.lower().strip(): v for k, v in row.items()}
            rows.append(normalized_row)
        return rows

    @staticmethod
    def preview_import(
        db: Session,
        rows: List[Dict[str, Any]],
        filename: str
    ) -> schemas.catalog_import.ImportPreview:
        """
        Generate a preview of the import actions.
        """
        preview_rows = []
        created_count = 0
        updated_count = 0
        conflict_count = 0
        error_count = 0
        
        batch_id = str(uuid.uuid4())

        for idx, row in enumerate(rows, start=1):
            try:
                sku = row.get("sku", "").strip() or None
                name = row.get("nombre", "").strip() or row.get("name", "").strip()
                
                if not name:
                    error_count += 1
                    preview_rows.append(schemas.catalog_import.ImportPreviewRow(
                        row_number=idx,
                        action=schemas.catalog_import.ImportAction.ERROR,
                        error="Missing name",
                        name="UNKNOWN"
                    ))
                    continue

                # 1. Try match by SKU
                existing_product = None
                if sku:
                    existing_product = db.query(models.Product).filter(
                        models.Product.sku == sku
                    ).first()

                # 2. Try match by Name if no SKU match
                if not existing_product:
                    existing_product = db.query(models.Product).filter(
                        models.Product.name.ilike(name)
                    ).first()
                
                # Determine action
                action = schemas.catalog_import.ImportAction.CREATE
                existing_id = None
                existing_name = None
                changes = []

                if existing_product:
                    existing_id = existing_product.id
                    existing_name = existing_product.name
                    
                    if sku and existing_product.sku != sku:
                        # Name matches but SKU is different -> potential conflict
                        action = schemas.catalog_import.ImportAction.CONFLICT
                        conflict_count += 1
                    else:
                        action = schemas.catalog_import.ImportAction.UPDATE
                        updated_count += 1
                        # Detect basic changes
                        if existing_product.name != name:
                            changes.append(f"Name change: {existing_product.name} -> {name}")
                else:
                    created_count += 1
                
                preview_rows.append(schemas.catalog_import.ImportPreviewRow(
                    row_number=idx,
                    action=action,
                    sku=sku,
                    name=name,
                    existing_id=existing_id,
                    existing_name=existing_name,
                    changes=changes,
                    raw_data=row
                ))

            except Exception as e:
                error_count += 1
                preview_rows.append(schemas.catalog_import.ImportPreviewRow(
                    row_number=idx,
                    action=schemas.catalog_import.ImportAction.ERROR,
                    error=str(e),
                    name="ERROR"
                ))

        return schemas.catalog_import.ImportPreview(
            batch_id=batch_id,
            filename=filename,
            total_rows=len(rows),
            created_count=created_count,
            updated_count=updated_count,
            conflict_count=conflict_count,
            error_count=error_count,
            preview_rows=preview_rows
        )

    @staticmethod
    def commit_import(
        db: Session,
        preview_rows: List[schemas.catalog_import.ImportPreviewRow],
        update_stock: bool,
        actor_id: int,
        filename: str
    ) -> Dict[str, int]:
        """
        Execute the import based on preview rows.
        """
        # Create CSV Upload record for audit
        csv_upload = models.CsvUpload(
            filename=filename
        )
        db.add(csv_upload)
        db.flush()

        results = {"created": 0, "updated": 0, "failed": 0}

        for p_row in preview_rows:
            if p_row.action == schemas.catalog_import.ImportAction.ERROR:
                results["failed"] += 1
                continue
            
            row = p_row.raw_data
            sku = p_row.sku
            name = p_row.name
            
            product = None
            if p_row.existing_id:
                product = db.query(models.Product).filter(
                    models.Product.id == p_row.existing_id
                ).with_for_update().first()

            # Extra safety check for CONFLICT or new SKU
            if not product and sku:
                product = db.query(models.Product).filter(
                    models.Product.sku == sku
                ).with_for_update().first()

            if product:
                # UPDATE
                product.name = name
                product.sku = sku or product.sku
                product.categoria = row.get("categoria", row.get("category", product.categoria))
                product.unit = row.get("unidad", row.get("unit", product.unit)) or "Unidad"
                product.precio = float(row.get("precio", row.get("price", product.precio)))
                product.description = row.get("descripcion", row.get("description", product.description))
                product.imagen_url = row.get("imagen_url", row.get("image", product.imagen_url))
                results["updated"] += 1
            else:
                # CREATE
                product = models.Product(
                    sku=sku,
                    name=name,
                    categoria=row.get("categoria", row.get("category", "General")),
                    unit=row.get("unidad", row.get("unit", "Unidad")),
                    precio=float(row.get("precio", row.get("price", 0.0))),
                    description=row.get("descripcion", row.get("description", "")),
                    imagen_url=row.get("imagen_url", row.get("image", "/static/img/default-product.png")),
                    stock_actual=0,
                    source_csv_id=csv_upload.id
                )
                db.add(product)
                db.flush()
                results["created"] += 1
            
            if update_stock:
                stock_val = row.get("stock", row.get("stock_actual", "0"))
                try:
                    stock_int = int(stock_val)
                    if stock_int > 0:
                        # Use adjustment with explicit reason for bulk audit
                        InventoryService.adjust_stock(
                            db=db,
                            product_id=product.id,
                            new_quantity=stock_int,
                            actor_id=actor_id,
                            reason=f"Bulk Import Stock Update ({filename})"
                        )
                except (ValueError, TypeError):
                    pass

        csv_upload.products_created = results["created"]
        csv_upload.products_updated = results["updated"]
        db.commit()
        return results
