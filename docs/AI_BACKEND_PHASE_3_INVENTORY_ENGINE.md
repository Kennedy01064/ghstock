# AI Backend Phase 3 — Inventory Engine and Stock Ledger

## Phase Goal
Replace ad hoc stock mutations with a coherent inventory engine that is auditable, conflict-aware, and ready for web + mobile clients.

This phase turns inventory into a real domain subsystem, not just fields being incremented/decremented.

## In Scope
- Formalize inventory movement types.
- Introduce reservation and release behavior.
- Make stock mutations auditable.
- Remove silent corrections in inventory flows.
- Separate central inventory behavior from building inventory behavior.
- Make inventory write paths service-driven and transaction-safe.

## Out of Scope
- Full advanced forecasting.
- Procurement planning.
- Cross-warehouse optimization.
- Full partial dispatch UX semantics beyond what backend needs to support.

## Current Problems This Phase Must Solve
- Central stock is mutated directly without a consistent domain abstraction.
- Building inventory consumption can silently clamp to available quantity.
- Reservation does not exist before dispatch confirmation.
- Inventory movements are too limited for future operational flows.
- Manual adjustments are not expressed strongly enough as audit events.

## Design Principles
- Every stock mutation must have a type, actor, reference, and timestamp.
- Stock must never be reduced implicitly without audit context.
- Reservation must happen before dispatch finalization.
- Release must be possible when a dispatch path is interrupted.
- Building inventory and central inventory are related but not identical concerns.

## Target Concepts

### Central Inventory State
For each product, define at minimum:
- `on_hand_stock`
- `reserved_stock`
- `available_stock = on_hand_stock - reserved_stock`

If retaining `stock_actual` temporarily for compatibility, document whether it means:
- on-hand
- available
- or something transitional

Avoid ambiguous naming long-term.

### Movement Types
Minimum set:
- `purchase`
- `reserve`
- `release`
- `dispatch`
- `receive`
- `consume`
- `adjust`
- `return`
- `transfer_out`
- `transfer_in`
- `shrinkage`

### References
Every movement should be able to reference:
- purchase id
- order id
- dispatch batch id
- building inventory id or building id
- adjustment event id / reason context

## Concrete Tasks

### 1. Clarify Stock Model
Decide and document what current central stock fields mean.

Preferred target:
- keep `on_hand_stock`
- add `reserved_stock`
- derive `available_stock`

Transitional option:
- retain `stock_actual` as on-hand
- add `reserved_stock`
- compute available in service/schema layer

Acceptance:
- stock semantics are unambiguous in code and API

### 2. Introduce Reservation Flow
When eligible orders are consolidated or prepared for dispatch, reserve stock before final dispatch confirmation.

Rules:
- reservation cannot exceed available stock
- reservation must fail explicitly on shortage
- reservation creation must be auditable
- repeat reservation attempts must be conflict-safe

Acceptance:
- two operators cannot promise the same stock unknowingly

### 3. Introduce Release Flow
When a reservation becomes invalid, release must restore availability.

Examples:
- order removed from pending batch
- batch cancelled or reworked
- order rejected from batch
- reservation timed out in future evolution

Acceptance:
- reserved stock does not get stranded permanently

### 4. Make Dispatch Consume Reserved/Validated Stock
Dispatch confirmation should:
- validate batch eligibility
- consume reserved stock or atomically transition from available to dispatched
- create movement entries
- mark order/batch state in same transaction boundary

Acceptance:
- dispatch cannot oversell stock under concurrency

### 5. Fix Building Inventory Consumption Semantics
Consumption must not clamp silently.

Required behavior:
- if requested consume quantity > available building quantity, fail explicitly
- create consumption movement/log only on valid success

Acceptance:
- building inventory consumption is trustworthy and auditable

### 6. Formalize Adjustment Behavior
Adjustments must be modeled distinctly from consumption.

Required fields in future-compatible design:
- actor
- previous quantity
- new quantity or delta
- reason
- optional comment

Acceptance:
- manual correction is visibly different from real usage

### 7. Prepare Return / Transfer / Shrinkage Hooks
Even if not fully exposed in API this phase, shape the movement model so these can be added cleanly.

Acceptance:
- inventory design does not need to be broken again when post-dispatch lifecycle is implemented

## Suggested Service Boundaries
Suggested services:
- `InventoryService`
- `ReservationService` or reservation methods inside `InventoryService`
- `BuildingInventoryService`

Example responsibilities:
- reserve stock
- release stock
- apply purchase
- confirm dispatch consumption
- receive into building inventory
- consume from building inventory
- adjust stock with reason

## Transaction Guidance
Critical combined operations must happen in one transaction boundary:
- reservation across batch items
- dispatch confirmation
- order receipt into building inventory
- purchase creation with stock increase

Do not split stock mutation and movement logging into separate commits.

## Definition of Done
- stock semantics are documented and consistent
- reservation exists
- release exists
- dispatch stock mutation is transaction-safe
- building consumption no longer clamps silently
- adjustments are audit-oriented
- movement model is extensible for future flows

## Guidance for AI Agents
- Do not hide business errors by auto-correcting requested quantities.
- Do not update stock without a matching movement/audit record.
- Do not implement reservation as a UI-only idea; it must exist in backend logic.
- Prefer small, explicit services over clever implicit mutation.

## Deliverables Expected from an Implementation PR
- model/schema updates if needed
- migration files
- service-layer changes
- documented stock semantics
- note on backward compatibility for existing API consumers
