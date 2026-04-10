"""
One-time script to create the production superadmin user.
Run via: python backend/scripts/create_superadmin.py
"""
import sys
import os
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from backend.db.session import SessionLocal
from backend.models import User
from backend.core.security import get_password_hash

def create_superadmin():
    db = SessionLocal()
    try:
        existing = db.query(User).filter(User.username == "krojas").first()
        if existing:
            existing.password_hash = get_password_hash("krojas@gh")
            existing.role = "superadmin"
            existing.is_active = True
            db.commit()
            print("Usuario 'krojas' actualizado correctamente.")
        else:
            user = User(
                username="krojas",
                name="Kennedy Rojas",
                role="superadmin",
                password_hash=get_password_hash("krojas@gh"),
                is_active=True,
            )
            db.add(user)
            db.commit()
            print("Usuario 'krojas' creado correctamente.")
    except Exception as e:
        db.rollback()
        print(f"Error: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    create_superadmin()
