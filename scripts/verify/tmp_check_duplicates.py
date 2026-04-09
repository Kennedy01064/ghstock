import sqlite3

def check_duplicates():
    conn = sqlite3.connect('stock_local.db')
    cursor = conn.cursor()
    
    # Check BuildingInventory
    cursor.execute('''
        SELECT building_id, product_id, COUNT(*) 
        FROM building_inventory 
        GROUP BY building_id, product_id 
        HAVING COUNT(*) > 1
    ''')
    bi_dups = cursor.fetchall()
    print(f"BuildingInventory duplicates: {bi_dups}")
    
    # Check DispatchBatchItem
    cursor.execute('''
        SELECT batch_id, product_id, COUNT(*) 
        FROM dispatch_batch_item 
        GROUP BY batch_id, product_id 
        HAVING COUNT(*) > 1
    ''')
    batch_dups = cursor.fetchall()
    print(f"DispatchBatchItem duplicates: {batch_dups}")

    # Check multiple draft orders per building
    cursor.execute('''
        SELECT building_id, COUNT(*) 
        FROM "order" 
        WHERE status = 'draft' 
        GROUP BY building_id 
        HAVING COUNT(*) > 1
    ''')
    draft_dups = cursor.fetchall()
    print(f"Draft Order duplicates: {draft_dups}")

    # Check negative quantities
    cursor.execute('SELECT id, stock_actual FROM product WHERE stock_actual < 0')
    print(f"Negative product stock: {cursor.fetchall()}")
    
    cursor.execute('SELECT id, quantity FROM building_inventory WHERE quantity < 0')
    print(f"Negative building generic inventory: {cursor.fetchall()}")
    
    conn.close()

if __name__ == "__main__":
    check_duplicates()
