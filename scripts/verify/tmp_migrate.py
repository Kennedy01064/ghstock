import sqlite3
import os

db_path = "frontend/instance/stock.db"

if os.path.exists(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    columns = [
        ("source_url", "VARCHAR(512)"),
        ("is_dynamic", "BOOLEAN DEFAULT 0"),
        ("last_synced_at", "DATETIME")
    ]
    
    for col_name, col_type in columns:
        try:
            cursor.execute(f"ALTER TABLE product ADD COLUMN {col_name} {col_type}")
            print(f"Added column {col_name}")
        except sqlite3.OperationalError as e:
            if "duplicate column name" in str(e).lower():
                print(f"Column {col_name} already exists")
            else:
                print(f"Error adding {col_name}: {e}")
    
    conn.commit()
    conn.close()
    print("Migration completed.")
else:
    print(f"Database {db_path} not found.")
