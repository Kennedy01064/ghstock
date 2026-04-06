# AI Backend API Conventions

## Purpose
Define implementation conventions for the FastAPI backend so AI agents produce consistent API behavior.

## General Rules
- Keep FastAPI as the only business authority.
- Prefer explicit domain-oriented endpoints over frontend-driven ad hoc behavior.
- Avoid changing endpoint URLs unless there is a clear migration plan.
- Use response codes intentionally.
- Mutating operations must be safe under retries or clearly reject duplicates.

## Error Mapping
Use these as default semantics:

- `400 Bad Request`
  - malformed business input shape that passes basic parsing but fails request contract expectations
- `401 Unauthorized`
  - missing/invalid/expired authentication
- `403 Forbidden`
  - authenticated user lacks role or ownership privileges
- `404 Not Found`
  - entity genuinely does not exist
- `409 Conflict`
  - concurrency conflict, duplicate logical entity, invalid repeated action, insufficient stock under conflict semantics
- `422 Unprocessable Entity`
  - semantically invalid domain input, such as impossible quantity or invalid state transition request

## Response Design
- For read endpoints, prefer stable response models.
- For create endpoints, return the newly created resource when possible.
- Do not return an unrelated pre-existing resource from a create endpoint unless endpoint semantics explicitly document upsert/idempotent-create behavior.
- Use consistent keys for error payloads.

## Idempotency Guidance
Operations that should be idempotent or conflict-safe:
- submit order
- consolidate batch
- confirm dispatch
- receive order
- create purchase (optional, but strongly recommended if client retries are expected)

Strategies:
- explicit idempotency key header or field
- unique business constraints
- operation status check with conflict response on repeat

## Transaction Guidance
Wrap multi-entity mutations in explicit service-level transaction boundaries.

Examples:
- order submit
- dispatch confirm
- order receive
- purchase create
- stock adjustment with movement creation

Do not scatter commits across endpoint loops.

## Validation Guidance
- Reject invalid quantities explicitly.
- Reject state transitions explicitly.
- Reject ownership violations explicitly.
- Never silently clamp requested quantities.
- Never silently ignore invalid rows in critical write operations.

## Auth Guidance
- Use bearer token auth consistently for SPA/mobile clients.
- Backend must not trust the frontend for role enforcement.
- `/auth/me` should remain a cheap, authoritative identity endpoint.
- If refresh tokens are introduced later, keep contract clean and explicit.

## CORS Guidance
- No wildcard CORS in non-local environments.
- Environment-specific allowed origins only.
- Keep credential strategy clear and intentional.

## Versioning Guidance
- Keep `/api/v1` stable.
- Breaking changes should be additive first where possible.
- If a response shape must change, note it in a migration/change document.

## Suggested Domain Endpoint Behavior

### Orders
- create draft: either create new draft or fail with domain conflict, but be explicit
- add item: merge or reject duplicate product rows consistently
- submit: fail if empty or invalid
- cancel: fail on illegal states
- receive: must be conflict-safe against duplicate receipt

### Dispatch
- consolidate: only eligible orders
- confirm: stock check and stock mutation in one protected transaction
- reject order from batch: rebuild aggregates deterministically

### Inventory
- consume: fail if requested quantity exceeds available quantity
- adjust: require explicit reason in future phases
- add inventory: merge with existing logical row only if invariant is clear and protected by DB uniqueness

### Purchases
- create: all lines validated before any mutation is committed
- totals and stock effects must match line items

## Logging and Observability Guidance
For critical mutations, log enough context to reconstruct intent:
- actor id
- operation type
- entity ids
- quantities
- result status
- correlation/request id when available

## AI Agent Rules
- Do not introduce hidden side effects in GET endpoints.
- Do not commit partial work inside loops for critical mutations.
- Do not patch API semantics differently across similar modules.
- Prefer small, explicit request/response schemas over loosely typed blobs.
