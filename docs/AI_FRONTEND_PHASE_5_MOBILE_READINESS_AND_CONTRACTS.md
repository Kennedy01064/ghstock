# AI Frontend Phase 5 — Mobile Readiness and Contracts

## Phase Goal
Make the SPA structurally clean enough that future mobile clients can reuse the same backend contract understanding without frontend chaos.

## In Scope
- reusable composables for common module/API patterns
- consistent naming of module state
- reduce page-coupled logic
- document frontend assumptions about backend contracts
- improve portability of request/state patterns

## Out of Scope
- building the mobile app
- backend redesign not required for frontend contract clarity

## Current Problems This Phase Must Solve
- web pages often accumulate request logic that is too tied to route/view structure
- future mobile work benefits from having clear reusable contract-level patterns now
- duplicated API understanding across pages creates drift

## Concrete Tasks

### 1. Extract Reusable Contract Logic
Candidates:
- auth/session composables
- paginated list composables
- mutation-state composables
- shared API modules by domain

Acceptance:
- repeated patterns stop living only inside page components

### 2. Normalize Domain Naming in Frontend
- route names
- store/composable names
- API module names
- state flags

Acceptance:
- the frontend describes backend concepts consistently

### 3. Document Frontend Contract Assumptions
- required fields
- expected error semantics
- route/module/backend mapping
- known alias endpoints or transitional contracts

Acceptance:
- future frontend/mobile work has a clearer map of backend expectations

### 4. Reduce Page Coupling
- move reusable request/state logic out of individual view files where appropriate
- keep pages focused on composition and rendering

Acceptance:
- the SPA is cleaner and closer to a reusable client architecture