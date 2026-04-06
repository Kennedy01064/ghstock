import sqlite3
conn = sqlite3.connect('frontend/instance/stock.db')
c = conn.cursor()
c.execute("UPDATE 'order' SET status = 'pending' WHERE status = 'draft';")
conn.commit()
print("Updated orders to pending.")
