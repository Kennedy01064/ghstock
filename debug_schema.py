import sqlite3

conn = sqlite3.connect('stock.db')
cursor = conn.cursor()
cursor.execute("PRAGMA table_info(user)")
cols = cursor.fetchall()
for col in cols:
    print(col)
conn.close()
