from app import create_app
from app.extensions import db
from sqlalchemy import text

app = create_app()
with app.app_context():
    try:
        db.session.execute(text("ALTER TABLE building ADD COLUMN imagen_frontis VARCHAR(255);"))
        db.session.commit()
        print("Migration successful")
    except Exception as e:
        print("Error:", e)
