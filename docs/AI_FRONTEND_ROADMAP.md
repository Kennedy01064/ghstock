# AI Frontend Roadmap

## Objective
Refactor `frontend-spa` into a resilient, role-aware, API-driven Vue client that cleanly supports the hardened FastAPI backend and prepares the codebase for eventual mobile parity.

## Architectural Direction
- Vue SPA is a client, not a second business engine.
- Pinia owns shared session and module state where needed.
- Router owns access flow and route-level control.
- Axios/shared API layer owns transport and error normalization.
- FastAPI remains the authority for workflow, stock, permissions, and validation.

## Phase Order

### Phase 1 — Foundation and Auth
Goal:
stabilize app bootstrap, session lifecycle, route guarding, and frontend build correctness.

Scope:
- app bootstrap review
- auth initialization flow
- route guard hardening
- role-aware redirects and navigation assumptions
- Vite/Tailwind alignment with actual SPA structure

Done when:
- app starts cleanly
- route access is coherent
- auth bootstraps predictably
- build config matches the real SPA

### Phase 2 — API Client and Error Handling
Goal:
make all frontend/backend communication robust and predictable.

Scope:
- timeout strategy
- normalized transport errors
- 401/403/409/422 handling
- shared request behavior
- auth session invalidation flow
- request configuration conventions

Done when:
- requests fail consistently
- auth expiry is handled coherently
- views no longer duplicate transport error parsing

### Phase 3 — Operational Modules
Goal:
align each operational module with the real backend contracts.

Scope:
- catalog
- buildings/admin management
- orders
- dispatch
- inventory
- purchases

Done when:
- screens and stores reflect backend contracts correctly
- critical actions prevent duplicate submits
- module behaviors are consistent with backend workflows

### Phase 4 — Resilience and UX States
Goal:
remove brittle UX around loading, conflicts, retries, and empty states.

Scope:
- loading states
- disabling critical actions in-flight
- conflict messaging
- retry-safe UX
- empty/error/partial states
- list/query states

Done when:
- critical operational screens behave safely under slow network or backend conflicts

### Phase 5 — Mobile Readiness and Contracts
Goal:
make the SPA codebase clean enough that mobile can reuse the backend contract model with minimal friction.

Scope:
- composable extraction
- reusable API modules
- state naming consistency
- route/view contract consistency
- reduce page-coupled logic
- document frontend API assumptions

Done when:
- the SPA is structurally prepared for future mobile parity without pretending to be the mobile app itself

## Critical Risks This Roadmap Must Reduce
- stale session after token expiry
- unauthorized route access through direct URL entry
- duplicated error parsing across pages
- UI assuming invalid backend state transitions
- duplicate submits creating duplicate operational intent
- legacy build config still pointing to removed frontend structure
- module pages using inconsistent endpoint or payload assumptions