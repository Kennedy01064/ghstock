import sqlite3
from passlib.hash import pbkdf2_sha256
from sqlalchemy import create_engine, MetaData, Table

# Generate password hash correctly
pwd_hash = pbkdf2_sha256.hash('password')
print("Hash generated:", pwd_hash)

conn = sqlite3.connect('dev_stock.db')
cursor = conn.cursor()

# Update all users to have 'password' as password
cursor.execute("UPDATE user SET password_hash = ?", (pwd_hash,))
conn.commit()
print("Passwords updated successfully!")

cursor.execute("SELECT username, password_hash FROM user")
print(cursor.fetchall())
conn.close()
