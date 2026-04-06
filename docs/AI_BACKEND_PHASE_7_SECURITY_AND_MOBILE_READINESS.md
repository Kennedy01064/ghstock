# AI Backend Phase 7 — Security, Observability, and Mobile Readiness

## Phase Goal
Prepare the backend to operate safely and predictably as the durable core for the SPA and future mobile clients.

This phase is about operational maturity, client durability, and production readiness.

## In Scope
- Authentication lifecycle hardening.
- Token/session strategy decisions for SPA + mobile.
- Request correlation and structured logging.
- Rate limiting strategy.
- Auditability improvements.
- Integration-test readiness for critical flows.
- Stable API contract mindset for multiple clients.

## Out of Scope
- Full SIEM integration.
- Enterprise IAM federation unless explicitly requested.
- Mobile app implementation itself.
- Frontend-specific UX redesign.

## Current Problems This Phase Must Solve
- Default security posture is too permissive for production.
- Auth lifecycle is minimal for multi-client durability.
- Logging and observability are not yet rich enough for hard backend operations.
- Rate protection strategy is not formalized.
- Critical business flows are not yet shaped for stable multi-client consumption and operational debugging.

## Design Principles
- Backend must be safe by default in non-local environments.
- SPA and mobile are first-class clients, not special cases.
- Critical mutations must be observable.
- Authentication failures and domain conflicts must be distinguishable.
- API contracts should evolve predictably.

## Core Security Topics

### 1. Auth Lifecycle Hardening
Decide and document strategy for:
- bearer access tokens
- token expiration behavior
- optional refresh token flow for SPA/mobile
- logout semantics
- handling compromised sessions

Rules:
- backend remains authoritative
- role checks stay server-side
- client convenience must not weaken backend controls

### 2. CORS and Environment Safety
Requirements:
- no permissive wildcard origins outside local development
- environment-driven allowed origin list
- explicit separation between local/dev/staging/prod expectations

### 3. Auditability
Critical operations should record enough context to reconstruct intent and result:
- actor id
- request/correlation id when available
- operation type
- entity ids
- quantity deltas or state deltas
- result

### 4. Rate Limiting Strategy
Define backend protection for:
- login attempts
- expensive import routes
- critical mutation endpoints if exposed to automation risk

### 5. Observability
Introduce or improve:
- structured logs
- request IDs / correlation IDs
- predictable error payloads
- operation-level logging for high-risk mutations

## Concrete Tasks

### 1. Harden Configuration Defaults
Requirements:
- production must not boot with insecure defaults
- secret/key settings must be explicit
- environment modes must be well defined
- CORS must be locked down outside local

Acceptance:
- production safety no longer depends on remembering to override dev defaults

### 2. Decide Auth Contract for SPA + Mobile
At minimum document and implement stable behavior for:
- login
- `/auth/me`
- expired token behavior
- unauthorized response semantics

If refresh tokens are introduced, do so explicitly and consistently.
If not introduced yet, document that choice clearly.

Acceptance:
- SPA and mobile can implement auth flow predictably

### 3. Add Request Correlation
Requirements:
- generate or accept request IDs
- include request ID in logs and error context where practical
- keep it consistent across critical operations

Acceptance:
- debugging a failed workflow across logs becomes practical

### 4. Improve Structured Logging
Log high-risk operations such as:
- purchase create
- order submit
- batch consolidate
- dispatch confirm
- receive order
- inventory consume/adjust/transfer/return/shrinkage

Acceptance:
- operators can explain what happened after the fact

### 5. Define Rate Limiting / Abuse Protection Strategy
Even if full implementation is deferred, backend design must clearly identify:
- routes to protect
- strategy/tooling to use
- expected behavior under abuse or burst retries

Acceptance:
- security posture is intentional, not accidental

### 6. Prepare Integration-Test Surface
Critical flows that should be integration-test ready:
- create/reuse draft order behavior
- submit order
- consolidate batch
- confirm dispatch
- receive order
- consume building inventory
- create purchase
- import preview/commit flow

Acceptance:
- backend architecture makes these flows straightforward to test

### 7. Stabilize API Change Discipline
Requirements:
- keep `/api/v1` coherent
- document contract changes when unavoidable
- avoid casual response-shape drift

Acceptance:
- SPA/mobile clients are not destabilized by backend churn

## Suggested Service/Infrastructure Boundaries
Potential additions:
- request ID middleware
- audit logging helper/service
- auth/session policy helper
- rate-limit integration hook

## Definition of Done
- environment defaults are hardened
- auth behavior is explicit for SPA/mobile clients
- request correlation exists or is clearly prepared
- structured logging is improved for critical mutations
- rate limiting strategy is defined or implemented where feasible
- critical backend flows are integration-test ready
- API contract discipline is documented and enforced

## Guidance for AI Agents
- Do not weaken security for local convenience in production-facing paths.
- Do not hide auth ambiguity behind frontend workarounds.
- Do not add logging that leaks secrets or sensitive payloads.
- Keep observability useful for operations, not noisy without structure.

## Deliverables Expected from an Implementation PR
- config/security changes
- middleware/logging changes if applicable
- auth contract notes
- rate limiting strategy notes
- integration-test readiness notes
- compatibility notes for SPA/mobile clients
