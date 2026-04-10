# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Full-stack inventory/stock management system for Grupo Hernandez. Python FastAPI backend + Vue 3 SPA frontend. Manages product catalogs, orders, dispatch batches, per-building inventory, and audit logs with JWT-based RBAC.

## Development Commands

### Backend

```bash
# Start dev server
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000

# Database migrations
alembic upgrade head
alembic downgrade -1
alembic revision --autogenerate -m "Description"

# Seed database
python backend/scripts/seed_db.py       # local dev
python backend/scripts/ci_seed.py       # CI test data (3 users, 2 buildings, sample products)
```

### Frontend

```bash
cd frontend-spa

npm install
npm run dev          # Dev server at http://localhost:5173 with HMR
npm run build        # Production build → dist/
npm run preview      # Preview production build

# E2E tests (Playwright)
npm run test:e2e
npm run test:e2e:ui
npx playwright install --with-deps   # One-time browser setup
```

### Running a single E2E test

```bash
cd frontend-spa
npx playwright test tests/auth.spec.js
npx playwright test tests/smoke.spec.js
```

## Architecture

### Backend (`backend/`)

**Layered architecture:**

1. **API Routes** (`backend/api/v1/endpoints/`) — 12 router modules (auth, catalog, inventory, orders, dispatch, users, superadmin, analytics, buildings, purchase, operations, media). All prefixed at `/api/v1`.

2. **Services** (`backend/services/`) — Business logic per domain: `order_service.py`, `dispatch_service.py`, `inventory_service.py`, `building_inventory_service.py`, `audit_service.py`, `catalog_import_service.py`, `purchase_service.py`.

3. **Models** (`backend/models.py`) — 14+ SQLAlchemy ORM models in a single file. Key entities: User, Building, Product, Order/OrderItem, DispatchBatch/DispatchBatchItem, InventoryMovement, BuildingInventory, ConsumptionLog, Purchase, SystemSetting, AuditLog.

4. **Database** (`backend/db/`) — `session.py` (SessionLocal factory), `bootstrap.py` (table creation), `runtime_schema.py` (`ensure_runtime_schema()` called on app startup).

5. **Core** (`backend/core/`) — `config.py` (env-based Settings), `security.py` (JWT + bcrypt + RBAC).

6. **Dependencies** (`backend/api/deps.py`) — FastAPI dependency injection: `get_current_user()`, `get_current_active_superadmin()`, `get_current_active_management()`, plus system lockdown guards.

**Auth flow:** Username + password → JWT (HS256) + refresh token persisted in DB → `Authorization: Bearer <token>` header.

**Roles:** `superadmin` > `admin` > `manager` — enforced at dependency injection layer, not route level.

### Frontend (`frontend-spa/src/`)

**Pinia stores** are the single source of truth — 10 stores: `authStore`, `productStore`, `ordersStore`, `dispatchStore`, `buildingStore`, `inventoryStore`, `userStore`, `systemStore`, `dashboardStore`, `uiStore`. Stores initialize asynchronously on app mount (`main.js`).

**Router** (`src/router/index.js`) — Route guards check auth state and user role from `authStore`. Views are lazy-loaded.

**API client** (`src/api/`) — Centralized Axios instance. Base URL from `VITE_API_BASE_URL` env var. Handles token refresh via interceptors.

**Key conventions:**
- Use `isSubmitting` flag in stores to prevent double-click submissions.
- Data from backend → frontend always passes through `src/utils/normalizers.js`.
- Display formatting (dates, currency, numbers) via `src/utils/formatters.js`.

### Order Workflow

Draft → Submit → Processing → Partially Dispatched → Dispatched → Delivered

- One draft order per building (enforced via DB unique index).
- `OrderItem.fulfilled_quantity` tracks partial dispatch.
- Dispatch batches aggregate items from multiple orders and reduce stock, creating `InventoryMovement` records.
- All mutations write to `AuditLog`.

### Database

SQLite for local/dev, PostgreSQL for production. Schema managed with Alembic.

**Two inventory tables:**
- `InventoryMovement` — global stock change log (all movements)
- `BuildingInventory` — per-building current stock levels

## Key Configuration

**Environment variables** (see `.env.example`):
- `ENVIRONMENT` — `local` | `development` | `staging` | `production`
- `SECRET_KEY` — JWT signing key (min 32 chars in production)
- `DATABASE_URL` — SQLite URI (local) or PostgreSQL URI (production)
- `BACKEND_CORS_ORIGINS` — comma-separated allowed origins
- `VITE_API_BASE_URL` — consumed by frontend Vite build

Production mode enforces non-SQLite DB and 32+ char `SECRET_KEY` at startup.

**Playwright config** (`playwright.config.js`): base URL `http://localhost:5173`, auth state stored in `playwright/.auth/user.json` (persists login across tests), 60s timeout, artifacts on failure.

## Common Extension Patterns

**New API endpoint:** Add router in `backend/api/v1/endpoints/`, register in `backend/api/api.py`, add Pydantic schemas in `backend/schemas/`.

**New Pinia store:** Create in `src/stores/`, initialize in `main.js` if async startup needed, import directly in views/components.

**Database schema change:** `alembic revision --autogenerate -m "description"` → review generated migration → `alembic upgrade head` → update models and services as needed.

**New E2E test:** Add `.spec.js` in `frontend-spa/tests/`. Reuse stored auth state from `playwright/.auth/user.json` to skip login.
