# AI Frontend Implementation Rules

## Purpose
This file defines execution rules for AI coding agents working on `frontend-spa`.

These rules are operational. Follow them during every frontend refactor phase.

## Primary Objective
Make the Vue SPA a resilient, role-aware, API-driven client for the FastAPI backend and a clean precursor to future mobile clients.

## Non-Negotiable Rules
- FastAPI is the source of truth.
- Do not move business logic into the SPA.
- Do not hide backend weaknesses with frontend workarounds.
- Do not invent stock calculations the backend does not expose.
- Do not assume success for critical mutations.
- Do not swallow backend conflicts silently.
- Do not leave route access control based only on menu visibility.

## Refactor Scope Rules
- Work in phases.
- Keep each PR/change set small and focused.
- Do not mix foundation cleanup with large UX redesign unless inseparable.
- If a route, state shape, or API usage pattern changes, document it.

## Coding Structure Rules
- Views render and orchestrate page-level behavior.
- Stores own shared session/module state.
- Composables own reusable request or interaction logic.
- API client centralizes transport concerns.
- Components should not embed duplicated request/error patterns.

## Router Rules
- Route protection must be explicit.
- Guest-only vs auth-required logic must remain centralized.
- Role-sensitive screens should use route meta and guard logic, not only component-level checks.
- Redirect behavior after login/logout should be deterministic.

## Session Rules
- Session storage/local storage behavior must be intentional.
- Expired or invalid tokens must leave the SPA in a coherent state.
- 401 handling must not leave stale protected UI active.
- Clearing auth must also clear any dependent privileged state where needed.

## API Rules
- All HTTP requests should flow through a shared client or clearly shared request utility.
- Timeouts should be explicit.
- Duplicate error normalization logic should be removed.
- Backend `409`, `422`, `403`, `404`, `401` must be distinguishable in UI handling.
- Do not use ad hoc endpoint paths inline everywhere if shared modules can centralize them.

## UX Safety Rules
For critical write actions:
- prevent double-submit
- show in-flight state
- handle retry failure explicitly
- surface backend conflict meaningfully
- do not leave buttons enabled while the request is still mutating critical state unless intentional

## Build Rules
- Vite config must reflect the actual SPA structure.
- Tailwind scanning must point to the SPA source files, not legacy removed frontends.
- Environment variables must be explicit and documented.
- The app should not depend on undeclared runtime assumptions.

## Mobile-Readiness Rules
- Avoid web-only assumptions in core module logic where possible.
- Prefer reusable composables and API modules over deeply page-coupled logic.
- Keep contract and state naming stable enough that a mobile client could reuse the same API understanding.

## Anti-Patterns AI Agents Must Avoid
- role checks scattered across random components
- error parsing duplicated in multiple views
- direct localStorage reads everywhere
- optimistic UI for critical inventory or dispatch actions without backend confirmation
- hidden API calls inside deeply nested presentational components
- giant visual redesign mixed with transport/auth fixes
- adding frontend state machines that disagree with backend workflow

## Preferred Delivery Style
When implementing a phase:
- start with a short execution plan
- touch only the files needed
- keep changes coherent
- explain intentional tradeoffs
- leave clear next steps for the following phase