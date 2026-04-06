# AI Backend Phase 6 — Purchases and Catalog Imports

## Phase Goal
Make purchases and bulk catalog operations safe, atomic, reviewable, and auditable so they stop being a source of silent data corruption.

This phase is about bulk-write correctness and operational predictability.

## In Scope
- Atomic purchase creation.
- Validation-before-write for purchase lines.
- Safer CSV/catalog import flow.
- Preview/staging design for imports.
- Explicit product matching rules.
- Separation between catalog metadata updates and stock updates.

## Out of Scope
- Supplier optimization.
- Forecasting and replenishment planning.
- Pricing strategy engines.
- Frontend redesign beyond backend contract support.

## Current Problems This Phase Must Solve
- Purchases can currently ignore invalid lines instead of failing cleanly.
- Import logic can merge products too loosely.
- Catalog import behavior is too coupled to direct write/merge semantics.
- Bulk operations are not reviewable enough before commit.
- Product metadata updates and operational stock changes are not clearly separated.

## Design Principles
- Purchases are all-or-nothing.
- Invalid critical rows must fail the operation, not be skipped silently.
- Bulk import should be previewed before commit.
- Matching strategy must be explicit and predictable.
- Catalog metadata changes are not the same thing as stock events.

## Core Concepts

### Purchase
A purchase is an auditable inventory-increasing event.

Rules:
- all lines must validate before any stock mutation is committed
- purchase totals must match item totals
- stock increase must create movement records
- actor and supplier context must be preserved

### Catalog Import
Catalog import is a metadata synchronization or product creation process.

Rules:
- import should support preview/staging
- matching must be explicit
- ambiguous collisions should not be silently auto-resolved
- import should not be used as a hidden operational stock adjustment mechanism

## Concrete Tasks

### 1. Make Purchase Creation Atomic
Requirements:
- validate all items first
- fail if any product is missing/invalid
- fail if any quantity or unit price is invalid
- only commit once the full payload is valid
- stock updates and movement creation must happen in same transaction boundary

Acceptance:
- purchase creation never partially succeeds

### 2. Normalize Purchase Validation Errors
Requirements:
- explicit line-level validation feedback
- domain-aware error semantics
- no silent skipping of bad lines

Acceptance:
- operators can trust purchase failures and success responses

### 3. Separate Catalog Metadata from Stock Mutation
Requirements:
- import should update product metadata deliberately
- stock changes should go through inventory/purchase semantics, not metadata import shortcuts
- if stock import is retained, it must be clearly labeled and separately controlled

Acceptance:
- catalog imports do not quietly perform operational stock changes without clear intent

### 4. Add Import Preview / Staging Design
Preferred design:
- upload file
- parse and validate
- produce preview result
- flag creates/updates/conflicts/errors
- only then commit changes

If full staging implementation is deferred, at minimum define backend contract and structure for it.

Acceptance:
- import flow is reviewable and extensible

### 5. Make Matching Rules Explicit
Matching priority should be deliberate, for example:
1. SKU exact match
2. optional explicit external source identifier
3. name-based matching only if explicitly enabled and safe

Requirements:
- ambiguous collisions must be flagged
- AI agents must not “guess” product identity destructively

Acceptance:
- product matching behavior is predictable and documented

### 6. Preserve Import Audit Context
Each bulk import should preserve:
- upload identifier
- actor
- file/source name
- create/update counts
- validation/conflict summary

Acceptance:
- bulk data changes can be explained later

## Suggested Service Boundaries
Suggested services:
- `PurchaseService`
- `CatalogImportService`

Responsibilities:
- validate purchase payloads
- create purchases atomically
- apply stock increase with audit trail
- parse import rows
- preview import effects
- commit import changes
- handle matching/conflict rules

## Transaction Guidance
The following must be atomic:
- purchase creation + purchase items + stock increase + movement creation
- import commit step if multi-row changes are applied after preview

Do not commit partial rows inside loops for critical write flows.

## Definition of Done
- purchases are atomic
- invalid purchase rows do not get skipped silently
- import matching rules are explicit
- import flow supports preview/staging design or contract
- metadata updates are separated from operational stock semantics
- import/audit context is preserved

## Guidance for AI Agents
- Do not keep partial-success behavior for purchases.
- Do not let name-only matching silently mutate the wrong product.
- Do not use import as a shortcut for bypassing inventory rules.
- Prefer reviewable bulk operations over clever direct writes.

## Deliverables Expected from an Implementation PR
- service-layer purchase/import changes
- any migration/model changes required
- import preview/staging contract notes
- compatibility notes for SPA consumers
- explicit documentation of matching rules
