import os
import shutil
from app import create_app
from app.extensions import db
from app.models import Building

app = create_app()

source = r"C:\Users\HP\.gemini\antigravity\brain\ef824119-f042-42c4-9ce1-bc264b1b650d\mockup_torre_norte_1773943487254.png"
dest_dir = r"c:\Users\HP\Desktop\Stock\app\static\uploads"
os.makedirs(dest_dir, exist_ok=True)
dest = os.path.join(dest_dir, "mockup_torre_norte.png")
shutil.copy(source, dest)

with app.app_context():
    b = Building.query.filter_by(name='Torre Norte').first()
    if b:
        b.imagen_frontis = 'mockup_torre_norte.png'
        db.session.commit()
        print("Updated Torre Norte image successfully!")
    else:
        print("Torre Norte not found.")
