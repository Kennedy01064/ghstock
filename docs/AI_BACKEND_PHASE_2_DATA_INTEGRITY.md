# AI Backend Phase 2 — Data Integrity and Invariants

## Phase Goal
Enforce the core business invariants at the database and service level before expanding more workflows.

This phase is about making the current model safer under real concurrency and repeated requests.

## In Scope
- Add missing unique constraints and indexes.
- Enforce single logical row per invariant-sensitive entity.
- Add defensive quantity constraints.
- Introduce explicit conflict semantics where current code relies on optimistic assumptions.
- Prepare optimistic locking or equivalent conflict-detection strategy.

## Out of Scope
- Full stock reservation engine.
- Full ledger redesign.
- Partial dispatch/backorder.
- Returns/transfers/shrinkage.

## Current Integrity Gaps This Phase Must Solve
- Duplicate building inventory rows are possible for the same building/product.
- Duplicate dispatch batch aggregate rows are possible for the same batch/product.
- Single active draft order per building is not protected strongly enough.
- Current flows rely on query-then-create patterns that can race.
- Quantities and state transitions are not defended by enough structural rules.

## Target Invariants to Enforce

### Building Inventory
Invariant:
- one row per `(building_id, product_id)`

Implementation:
- unique constraint on `(building_id, product_id)`
- service logic must merge intentionally rather than rely on duplicates

### Dispatch Batch Items
Invariant:
- one row per `(batch_id, product_id)`

Implementation:
- unique constraint on `(batch_id, product_id)`
- any recalculation logic should rebuild deterministically

### Draft Orders
Invariant:
- at most one active `draft` order per building

Implementation options:
1. partial unique index if supported by chosen database
2. status-normalized helper strategy
3. idempotency key or explicit conflict behavior in service layer

Preferred:
- DB-level uniqueness where feasible
- service-level explicit conflict fallback where partial indexes are not portable

### Positive Quantities
Invariant:
- order item quantity > 0
- purchase item quantity > 0
- dispatch aggregate quantity > 0
- building inventory quantity >= 0
- central product stock >= 0

Implementation:
- DB check constraints where possible
- service validation with explicit domain errors

## Concrete Tasks

### 1. Add Unique Constraints / Indexes
Add or prepare migrations for:
- `building_inventory(building_id, product_id)` unique
- `dispatch_batch_item(batch_id, product_id)` unique
- supporting indexes for frequent filters on order state, building, product, created_at

Acceptance:
- the database rejects duplicate logical rows

### 2. Harden Draft Order Creation
Current draft creation behavior should be made conflict-safe.

Required behavior:
- if a draft exists for the building, be explicit about whether the endpoint is:
  - idempotent-create returning the same draft
  - or conflicting with 409
- whichever rule is chosen must be documented and stable

Acceptance:
- repeated draft-creation attempts do not create multiple drafts

### 3. Add Defensive Constraints on Quantities
- prevent negative stock values where practical
- prevent zero/negative quantities for transactional item rows
- fail explicitly on invalid values

Acceptance:
- impossible quantity states cannot persist silently

### 4. Introduce Conflict Detection Strategy
For records vulnerable to concurrent updates, introduce one of:
- optimistic version field
- row locking in services
- explicit compare-and-set style updates

Priority candidates:
- product stock
- building inventory
- orders undergoing state transition
- dispatch batches undergoing confirmation

Acceptance:
- concurrency handling strategy is visible and intentional, not accidental

### 5. Normalize Domain Conflict Errors
Use explicit domain errors for:
- duplicate draft
- duplicate inventory row
- duplicate batch item
- stale update / concurrent modification
- invalid repeated state transition

Acceptance:
- integrity failures do not surface as generic 500s

## Suggested Migration Strategy
1. inspect existing data for duplicates
2. write cleanup/data migration if duplicates already exist
3. add unique constraints only after cleanup
4. deploy service-layer protections with the migration

## Data Cleanup Rules (If Existing Duplicates Are Found)
- `building_inventory`: merge duplicate rows by summing quantity only if business semantics confirm this is safe; otherwise stop and require manual resolution
- `dispatch_batch_item`: rebuild aggregates from orders in batch rather than trusting duplicate rows
- `draft orders`: preserve the newest valid draft or require manual resolution if multiple drafts contain meaningful divergent state

AI agents must not guess destructive cleanup blindly.

## Definition of Done
- uniqueness enforced for core logical entities
- draft creation is conflict-safe
- negative/impossible quantities are blocked
- conflict errors are explicit
- migrations include any necessary cleanup path

## Guidance for AI Agents
- Prefer additive schema changes first.
- Do not drop data unless a manual migration plan is documented.
- Do not mix reservation logic into this phase.
- Keep this phase focused on correctness, not UX convenience.

## Deliverables Expected from an Implementation PR
- migration files
- service updates for conflict-safe behavior
- data-cleanup notes if required
- explicit list of newly enforced invariants
