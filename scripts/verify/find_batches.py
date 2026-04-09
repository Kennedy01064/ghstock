import os
import sys
sys.path.append(os.path.abspath('./frontend'))
from app import create_app
from app.models.dispatch import DispatchBatch

app = create_app()

with app.app_context():
    batches = DispatchBatch.query.all()
    print("Found batches:", [(b.id, b.status) for b in batches])

