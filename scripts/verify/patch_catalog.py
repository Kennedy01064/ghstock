import os

target = r'c:\Users\HP\Desktop\Stock\backend\api\v1\endpoints\catalog.py'
with open(target, 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 1. Add import
for i, line in enumerate(lines):
    if 'from backend.services.scraper import ScraperService' in line:
        lines.insert(i + 1, 'from backend.services.inventory_service import InventoryService\n')
        break

# 2. Refactor create_product
for i, line in enumerate(lines):
    if 'def create_product(' in line:
        # Find the function body and replace
        start = i + 7 # line 82 usually
        for j in range(start, start + 10):
            if 'return product' in lines[j]:
                lines[start:j+1] = [
                    "    initial_stock = product_in.stock_actual\n",
                    "    product_data = product_in.model_dump()\n",
                    "    product_data['stock_actual'] = 0\n",
                    "    product = models.Product(**product_data)\n",
                    "    db.add(product)\n",
                    "    db.flush()\n",
                    "    if initial_stock > 0:\n",
                    "        InventoryService.adjust_stock(db=db, product_id=product.id, new_quantity=initial_stock, actor_id=current_user.id, reason='Initial Creation')\n",
                    "    db.commit()\n",
                    "    db.refresh(product)\n",
                    "    return product\n"
                ]
                break
        break

# 3. Refactor update_product
for i, line in enumerate(lines):
    if 'def update_product(' in line:
        start = i + 13 # around line 102
        for j in range(start, start + 20):
             if 'return product' in lines[j]:
                lines[start:j+1] = [
                    "    update_data = product_in.model_dump(exclude_unset=True)\n",
                    "    new_stock = update_data.pop('stock_actual', None)\n",
                    "    for field, value in update_data.items():\n",
                    "        setattr(product, field, value)\n",
                    "    db.flush()\n",
                    "    if new_stock is not None and new_stock != product.stock_actual:\n",
                    "        InventoryService.adjust_stock(db=db, product_id=product.id, new_quantity=new_stock, actor_id=current_user.id, reason='Manual Update')\n",
                    "    db.commit()\n",
                    "    db.refresh(product)\n",
                    "    return product\n"
                ]
                break
        break

with open(target, 'w', encoding='utf-8') as f:
    f.writelines(lines)

print("Catalog patched successfully.")
