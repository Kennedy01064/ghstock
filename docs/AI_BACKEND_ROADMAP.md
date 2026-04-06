# AI Backend Roadmap

## Objective
Refactor the backend into a production-ready FastAPI core that is safe for SPA + future mobile clients.

This file is written for AI coding tools (Antigravity/Codex-like agents). It is not a product brief. It is an execution guide.

## Non-Negotiable Architectural Direction
- FastAPI is the single source of truth.
- The frontend must consume FastAPI only.
- No business-critical logic should live in the SPA.
- Inventory consistency must be enforced in the backend and, where possible, in the database.
- All state transitions must be explicit and validated.
- Every stock change must be auditable.

## Phase Order

### Phase 1 — Foundation and Safety
Goal: remove fragile runtime behavior and prepare the codebase for controlled evolution.

Scope:
- Remove mutable bootstrap behavior from application startup.
- Introduce proper database migrations.
- Harden configuration by environment.
- Normalize domain/API error handling.
- Create service-layer structure for business logic.
- Keep external API behavior stable where possible.

Done when:
- App startup does not seed or mutate production data.
- Schema changes are handled by migrations.
- Secrets and CORS are environment-driven.
- New business logic can be implemented in services, not endpoints.

### Phase 2 — Data Integrity and Invariants
Goal: enforce core invariants at the persistence layer.

Scope:
- Unique inventory per building/product.
- Unique dispatch-batch item per batch/product.
- Single active draft per building.
- Defensive checks against invalid quantities.
- Add optimistic locking or equivalent conflict detection where needed.

Done when:
- Duplicate logical records cannot be created accidentally.
- Invalid domain states are blocked even under concurrency.

### Phase 3 — Inventory Engine and Stock Ledger
Goal: replace ad hoc stock mutation with auditable inventory mechanics.

Scope:
- Introduce stock ledger / movement strategy.
- Add reservation mechanics.
- Add release mechanics.
- Make consume/adjust operations explicit and atomic.
- Keep central and building inventory behavior distinguishable.

Done when:
- Every stock mutation has a reason and an auditable trail.
- Stock can be reserved before dispatch.
- Silent auto-corrections are removed.

### Phase 4 — Orders and Dispatch Workflow Hardening
Goal: formalize order and dispatch lifecycle.

Scope:
- Explicit order state machine.
- Explicit dispatch-batch state machine.
- Idempotent submit/consolidate/confirm/receive operations.
- Rejection and retry semantics.
- Prepare support for partial fulfillment and backorders.

Done when:
- Repeated requests do not corrupt state.
- Invalid transitions fail clearly.

### Phase 5 — Building Inventory Lifecycle
Goal: complete the local inventory loop for buildings.

Scope:
- Receipt confirmation.
- Consumption.
- Audited adjustment.
- Returns to central warehouse.
- Transfers between buildings.
- Shrinkage/loss events.

Done when:
- Building inventory has a full operational lifecycle.

### Phase 6 — Purchases and Catalog Imports
Goal: stop partial-success corruption and make bulk operations safe.

Scope:
- Purchases must be all-or-nothing.
- CSV import must have preview/staging behavior.
- Product matching rules must be explicit.
- Distinguish catalog metadata updates from operational stock changes.

Done when:
- Invalid purchase rows do not get ignored silently.
- Bulk imports are predictable and reviewable.

### Phase 7 — Observability, Security, and Mobile Readiness
Goal: make the backend robust enough for web + mobile.

Scope:
- Structured logs.
- Correlation/request IDs.
- Rate limiting strategy.
- Better auth lifecycle decisions.
- Integration tests for critical flows.
- Stable API contracts.

Done when:
- Backend behavior is observable and stable across multiple clients.

## Rules for AI Agents
- Do not mix multiple phases in a single large refactor unless explicitly asked.
- Prefer small commits with clear scope.
- Do not alter public endpoint contracts unnecessarily in Phase 1.
- Do not add frontend logic to compensate for backend consistency gaps.
- Favor explicit domain errors over generic HTTP 500 responses.
- Prefer additive migration steps over destructive schema rewrites.

## Critical Business Risks to Avoid
- Two users creating the same logical draft order.
- Two concurrent stock consumers overselling the same stock.
- Purchase creation that partially succeeds.
- Building inventory duplicates for the same building/product.
- Silent stock truncation or auto-adjustment without audit trail.
- Startup code mutating production data.

## Deliverable Style for Future AI Tasks
When implementing a phase, always output:
1. files created/modified
2. migration impact
3. behavior changes
4. rollback concerns
5. open risks
