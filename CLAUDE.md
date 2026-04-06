# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Stock management system (inventory, orders, dispatch) with a split architecture:
- **Backend**: FastAPI REST API (port 8000)
- **Frontend**: Flask web UI (port 5000)
- **Database**: Shared SQLite file at `frontend/instance/stock.db` (both apps access it via SQLAlchemy)

## Commands

### Setup
```bash
python -m venv venv
source venv/Scripts/activate   # Windows git-bash
pip install -r backend/requirements.txt
pip install -r frontend/requirements.txt
python backend/scripts/seed_db.py   # seed DB with test data
```

### Run
```bash
# Frontend (Flask)
cd frontend && python run.py          # http://localhost:5000

# Backend (FastAPI)
python -m uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
# Swagger docs at http://localhost:8000/docs
```

Both servers should run concurrently in separate terminals.

### Seed credentials
- superadmin: `superboss / password123`
- admins: `admin_juan / password123`, `admin_maria / password123`

## Architecture

### Dual-app, shared database
The frontend (Flask) and backend (FastAPI) each define their own SQLAlchemy models but point to the same SQLite file. **When changing a model, update both** `backend/models.py` and `frontend/app/models.py` to keep them in sync.

### Backend structure
- `backend/main.py` — App creation, middleware, exception handlers
- `backend/api/v1/api.py` — Router aggregation for all endpoint modules
- `backend/api/v1/endpoints/` — Route handlers (login, catalog, buildings, orders, dispatch)
- `backend/api/deps.py` — FastAPI dependencies (auth via JWT/OAuth2)
- `backend/core/config.py` — Settings (SECRET_KEY, DATABASE_URL, CORS)
- `backend/db/session.py` — Engine and SessionLocal factory
- `backend/schemas/` — Pydantic request/response models
- `backend/services/` — Business logic (e.g., scraper for dynamic product sync)

### Frontend structure
- `frontend/run.py` — Entry point
- `frontend/app/__init__.py` — Flask app factory (`create_app`), registers blueprints, auto-creates tables
- `frontend/app/blueprints/` — Five blueprints: auth, dashboard, catalog, orders, dispatch
- `frontend/app/templates/` — Jinja2 templates; `base.html` is the main layout
- `frontend/app/extensions.py` — SQLAlchemy and LoginManager initialization
- `frontend/config.py` — Flask config (SECRET_KEY, SQLALCHEMY_DATABASE_URI)

### Auth
- Backend: JWT tokens (HS256, 30 min expiry) via OAuth2PasswordBearer
- Frontend: Flask-Login session-based auth with werkzeug password hashing
- Roles: `superadmin` and `admin`; superadmin has a "view as admin" toggle

### Key domain models (13 tables)
User, Building, Product, CsvUpload, Order, OrderItem, DispatchBatch, DispatchBatchItem, InventoryMovement, BuildingInventory, ConsumptionLog, Purchase, PurchaseItem.

OrderItem stores snapshot fields (nombre_producto_snapshot, precio_unitario) for audit trail.

### Environment variables
| Variable | Default | Purpose |
|---|---|---|
| `SECRET_KEY` | dev fallback | JWT/session signing |
| `DATABASE_URL` | `sqlite:///./frontend/instance/stock.db` | DB connection string |

## Notes

- No automated tests exist yet.
- No Docker or CI/CD configuration.
- Alembic is in backend requirements but no migration directory is set up; tables are auto-created by Flask on startup.
- The UI language is Spanish.
