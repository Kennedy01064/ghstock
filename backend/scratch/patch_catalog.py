import os

file_path = r"c:\Users\HP\Desktop\Stock\backend\api\v1\endpoints\catalog.py"
with open(file_path, 'r', encoding='utf-8') as f:
    content = f.read()

# Try a very specific multi-line replacement
old_block = """    if q:
        query = query.filter(
            (models.Product.name.ilike(f"%{q}%")) | 
            (models.Product.sku.ilike(f"%{q}%"))
        )"""

# Instead of exact block, let's find the lines
lines = content.splitlines()
new_lines = []
found = False

for i in range(len(lines)):
    if 'models.Product.sku.ilike(f"%{q}%")' in lines[i]:
        # Check if next line is closing paren of filter
        if i+1 < len(lines) and '        )' == lines[i+1].strip():
            new_lines.append(lines[i] + ' |')
            new_lines.append('            (models.Product.barcode == q)')
            found = True
        else:
            new_lines.append(lines[i])
    else:
        new_lines.append(lines[i])

if found:
    with open(file_path, 'w', encoding='utf-8', newline='\n') as f:
        f.write('\n'.join(new_lines) + '\n')
    print("Patched via line scanning successfully.")
else:
    print("Could not find line to patch.")
