from backend.db.session import SessionLocal
from backend.models import DispatchBatch, Order

db = SessionLocal()
print(f'Batches: {db.query(DispatchBatch).count()}')
print('Orders:')
for o in db.query(Order).all():
    print(f' - ID: {o.id}, Status: {o.status}')
