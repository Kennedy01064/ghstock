# AI Frontend Phase 3 — Operational Modules

## Phase Goal
Align operational SPA modules with the real backend contracts and workflows.

## In Scope
- catalog module
- building/admin management screens
- orders screens
- dispatch screens
- inventory screens
- purchases screens

## Out of Scope
- global design system rebuild
- mobile app implementation
- backend contract redesign unless strictly necessary

## Current Problems This Phase Must Solve
- module pages may still assume old response shapes or old workflow behaviors
- duplicated request patterns likely exist across create/edit/detail/list pages
- critical operational actions need better in-flight safety
- backend now returns more explicit conflicts and the SPA must reflect them correctly

## Concrete Tasks

### 1. Audit Module-by-Module API Alignment
For each module:
- endpoint path correctness
- payload shape correctness
- response-shape expectations
- workflow-state assumptions

Acceptance:
- pages no longer depend on stale backend assumptions

### 2. Prevent Duplicate Critical Actions
Apply to:
- order submit/reopen/cancel
- dispatch confirm/reject
- inventory consume/adjust/transfer/return/shrinkage
- purchase create
- CSV import commit

Acceptance:
- critical mutations cannot be accidentally double-fired from normal UI behavior

### 3. Normalize Operational UX States
- loading
- saving
- conflict
- validation error
- forbidden
- empty data

Acceptance:
- operations behave predictably under backend conflict or validation failure

### 4. Clean Module Boundaries
- extract repeated module request helpers/composables where clearly beneficial
- avoid each view embedding transport logic differently

Acceptance:
- modules are easier to maintain and align with backend changes