from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend import models

DB_URL = "sqlite:///./stock.db"
engine = create_engine(DB_URL)
SessionLocal = sessionmaker(bind=engine)
db = SessionLocal()

user = db.query(models.User).first()
if user:
    print(f"Found user: {user.username}, ID: {user.id}")
else:
    print("No user found.")
