# AI Backend Phase 1 — Foundation and Safety

## Phase Goal
Stabilize the backend so future phases can be implemented safely.

This phase is about architecture hygiene, not feature expansion.

## In Scope
- Remove runtime bootstrap behavior from startup.
- Introduce migration-driven schema management.
- Harden settings and environment handling.
- Standardize error handling.
- Create a clear service-layer structure.
- Preserve current endpoint behavior as much as possible.

## Out of Scope
- Reservation engine.
- Major order workflow redesign.
- Partial dispatch.
- Returns/transfers/shrinkage.
- CSV staging redesign.

## Current Problems This Phase Must Solve
- Startup currently mutates state.
- Schema lifecycle is not controlled by migrations.
- Default development settings are unsafe for anything beyond local use.
- Business logic is too endpoint-centric.
- Generic exceptions are used where domain errors should exist.

## Target Folder Structure

Suggested structure:

```text
backend/
  api/
    deps.py
    v1/
      api.py
      endpoints/
  core/
    config.py
    exceptions.py
    security.py
    logging_middleware.py
  db/
    session.py
    base.py
  domain/
    errors.py
    enums.py
  services/
    __init__.py
    inventory_service.py
    order_service.py
    dispatch_service.py
    purchase_service.py
  repositories/
    __init__.py
    inventory_repository.py
    order_repository.py
    dispatch_repository.py
    purchase_repository.py
  models.py
  schemas/
alembic/
```

Note:
- Repositories are optional if the codebase stays small, but services are not optional.
- If repositories are not introduced now, service layer must still be introduced.

## Concrete Tasks

### 1. Stop Mutating Data on Startup
- Remove automatic seed/fix logic from `startup` execution path.
- Keep startup limited to app wiring and lightweight readiness concerns.
- If demo seed is still needed, move it to a dedicated script/CLI command.

Acceptance:
- Starting the app does not create users, buildings, products, or apply hidden fixes.

### 2. Introduce Alembic Migrations
- Initialize Alembic if missing.
- Create baseline migration from current models.
- Ensure all future schema changes happen through migrations.

Acceptance:
- Database schema can be reproduced through migrations only.

### 3. Harden Configuration
- Remove insecure defaults where possible.
- Split environment expectations clearly: local/dev/staging/prod.
- CORS must be environment-driven, not wildcard by default.
- Fail fast if required production settings are missing.

Acceptance:
- Production cannot accidentally run with permissive local defaults.

### 4. Introduce Domain Error Vocabulary
Create explicit domain errors such as:
- `DomainConflictError`
- `InvalidStateTransitionError`
- `InsufficientStockError`
- `DuplicateDraftOrderError`
- `EntityOwnershipError`
- `ValidationDomainError`

Map them consistently to HTTP responses:
- 400 for malformed business input
- 403 for forbidden ownership/role access
- 404 for missing entity
- 409 for state/data conflicts
- 422 for semantically invalid requests

Acceptance:
- Critical flow failures no longer collapse into generic 500-style behavior.

### 5. Create Service Layer Boundaries
Move business mutations out of endpoints, starting with:
- order submit/reopen/cancel/receive
- dispatch consolidate/confirm/reject
- inventory consume/adjust/add
- purchase create

Acceptance:
- Endpoints become orchestration-only.
- Business rules are testable without HTTP.

### 6. Prepare for Later Concurrency Controls
- Add clear transaction boundaries in services.
- Make places that need locking/versioning obvious and isolated.
- Do not fully implement reservation yet, but prepare code organization for it.

Acceptance:
- Future Phase 2/3 work can be layered on without rebreaking architecture.

## Suggested Implementation Order
1. Add domain errors and exception mapping.
2. Introduce services for the most mutation-heavy endpoints.
3. Remove startup seed/fix behavior.
4. Add Alembic and baseline migration.
5. Harden settings/CORS handling.
6. Clean imports and folder structure.

## Definition of Done
- No production data mutation on startup.
- Alembic baseline exists.
- Service layer exists for main mutating flows.
- Error mapping is explicit and domain-aware.
- Settings are environment-safe.
- Current API still works for the SPA with minimal contract churn.

## Guidance for AI Agents
- Prefer refactor without changing endpoint URLs in this phase.
- Do not redesign all models yet.
- Do not bundle data-integrity constraints into this phase unless required for migration setup.
- Keep commits scoped: startup, migrations, services, config, errors.

## Deliverables Expected from an Implementation PR
- code changes
- migration files
- `.env.example` updates if needed
- brief changelog of backend behavior changes
- note on any manual data migration required
