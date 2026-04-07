# AI Frontend Phase 2 — API Client and Error Handling

## Phase Goal
Make frontend/backend communication robust, explicit, and consistent.

## In Scope
- Axios client hardening
- timeout strategy
- normalized network/domain error handling
- auth-expiry handling
- 401 / 403 / 409 / 422 differentiation
- remove repeated request-error patterns where possible

## Out of Scope
- redesigning every module UI
- large store rewrite unless needed for transport coherence

## Current Problems This Phase Must Solve
- no explicit timeout in Axios
- 401 handling clears storage but may still leave UI state transitions too implicit
- pages can end up parsing and surfacing errors inconsistently
- conflict/validation semantics need to be treated as first-class UI outcomes

## Concrete Tasks

### 1. Add Timeout Strategy
- define default timeout in the shared client
- ensure timeout errors are distinguishable from backend responses

Acceptance:
- hanging requests no longer wait indefinitely

### 2. Strengthen Error Normalization
- preserve `status`, `detail`, and readable `message`
- distinguish 401 / 403 / 404 / 409 / 422 / timeout/network
- keep normalization centralized

Acceptance:
- views receive consistent error objects

### 3. Clarify 401 Flow
- clearing auth session must lead to coherent route/UI behavior
- avoid stale protected screens lingering after token expiry

Acceptance:
- expired session produces predictable logout-like behavior

### 4. Reduce Repeated Transport Patterns
- where obvious, extract shared request or mutation composables/helpers
- avoid each page reimplementing loading/error/reset patterns

Acceptance:
- transport concerns become more centralized and consistent