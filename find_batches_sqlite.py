import sqlite3
conn = sqlite3.connect('frontend/instance/stock.db')
c = conn.cursor()
c.execute("SELECT id, status FROM dispatch_batch;")
print("Baches:", c.fetchall())
