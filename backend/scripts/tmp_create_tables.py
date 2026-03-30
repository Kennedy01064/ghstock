from app import create_app
from app.extensions import db
from app.models import BuildingInventory, ConsumptionLog

app = create_app()

with app.app_context():
    print("Creating new tables...")
    BuildingInventory.__table__.create(db.engine, checkfirst=True)
    ConsumptionLog.__table__.create(db.engine, checkfirst=True)
    print("Tables created successfully.")
