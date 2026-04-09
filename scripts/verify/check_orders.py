import sqlite3
conn = sqlite3.connect('frontend/instance/stock.db')
c = conn.cursor()
c.execute("SELECT id, status, building_id FROM 'order';")
print("Orders:", c.fetchall())
