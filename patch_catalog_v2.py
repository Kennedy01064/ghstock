import os

target = r'c:\Users\HP\Desktop\Stock\backend\api\v1\endpoints\catalog.py'
with open(target, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Fix double line in update_product
for i, line in enumerate(lines):
    if "update_data = product_in.model_dump(exclude_unset=True)" in line:
        if i + 1 < len(lines) and "update_data = product_in.model_dump(exclude_unset=True)" in lines[i+1]:
            del lines[i+1]
            break

# 2. Refactor import_csv (lines 142+)
# We'll look for the loop starting at 'for row in parsed_rows:'
for i, line in enumerate(lines):
    if 'for row in parsed_rows:' in line:
        # Find where it ends (usually around the bulk operations)
        end_search = i + 1
        bulk_insert_idx = -1
        bulk_update_idx = -1
        for j in range(end_search, len(lines)):
             if 'db.bulk_insert_mappings(models.Product, insert_mappings)' in lines[j]:
                 bulk_insert_idx = j
             if 'db.bulk_update_mappings(models.Product, list(update_mappings.values()))' in lines[j]:
                 bulk_update_idx = j
             if 'new_upload.products_created =' in lines[j]:
                 loop_end = j
                 break
        
        # Replace the whole logic
        if bulk_insert_idx != -1:
            # We identified the block.
            new_logic = [
                "    for row in parsed_rows:\n",
                "        sku = row['sku']\n",
                "        name = row['name']\n",
                "        product = None\n",
                "        if sku:\n",
                "            product = db.query(models.Product).filter(models.Product.sku == sku).first()\n",
                "        if not product:\n",
                "            product = db.query(models.Product).filter(models.Product.name == name).first()\n",
                "\n",
                "        if product:\n",
                "            updated_count += 1\n",
                "            product.name = name\n",
                "            if sku: product.sku = sku\n",
                "            if row['unit']: product.unit = row['unit']\n",
                "            product.precio = row['precio']\n",
                "            if row['description']: product.description = row['description']\n",
                "            if row['categoria']: product.categoria = row['categoria']\n",
                "            if row['imagen_url']: product.imagen_url = row['imagen_url']\n",
                "\n",
                "            if row['stock_actual'] > 0:\n",
                "                InventoryService.adjust_stock(db=db, product_id=product.id, new_quantity=row['stock_actual'], actor_id=current_user.id, reason='CSV Import Update')\n",
                "        else:\n",
                "            created_count += 1\n",
                "            new_product = models.Product(\n",
                "                sku=sku or None,\n",
                "                name=name,\n",
                "                unit=row['unit'] or 'Unidad',\n",
                "                categoria=row['categoria'] or 'General',\n",
                "                precio=row['precio'],\n",
                "                description=row['description'] or None,\n",
                "                imagen_url=row['imagen_url'] or '/static/img/default-product.png',\n",
                "                stock_actual=0,\n",
                "                stock_minimo=10,\n",
                "                is_active=True,\n",
                "                source_csv_id=new_upload.id,\n",
                "                is_dynamic=False,\n",
                "            )\n",
                "            db.add(new_product)\n",
                "            db.flush()\n",
                "            if row['stock_actual'] > 0:\n",
                "                InventoryService.adjust_stock(db=db, product_id=new_product.id, new_quantity=row['stock_actual'], actor_id=current_user.id, reason='CSV Import Creation')\n"
            ]
            
            # Remove old logic (from loop start to after bulk calls)
            # Actually, I'll just replace the whole section from line 214 to 290 approx
            # But line numbers won't match exactly because of previous edits.
            # I'll use index based replacement.
            lines[i:loop_end] = new_logic
        break

with open(target, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Catalog fully patched.")
