# AI Frontend API Client Conventions

## Purpose
Define implementation conventions for the SPA transport layer so AI agents produce consistent request behavior.

## General Rules
- Prefer one shared Axios client.
- Normalize errors centrally.
- Distinguish auth failure from domain conflict from validation issues.
- Keep backend authority visible in UI error handling.
- Avoid inline duplicated request configuration across views.

## Base URL
- Base URL should come from `VITE_API_BASE_URL`.
- Local fallback may exist for development, but production assumptions must be explicit.
- Environment behavior should be documented.

## Timeout Strategy
- Client requests should use explicit timeouts.
- Timeouts should be long enough for operational calls but not indefinite.
- Timeout errors should surface clearly to the UI.

## Request Interceptor Rules
- Attach bearer token when present.
- Do not attach malformed auth headers.
- Keep request mutation minimal and predictable.
- Future request correlation headers may be added here if desired.

## Response Interceptor Rules
Normalize transport failures into a consistent frontend error shape.

Recommended normalized shape:
- `message`
- `status`
- `detail`
- `original`

Must distinguish:
- 401 unauthorized
- 403 forbidden
- 404 not found
- 409 conflict
- 422 validation/domain input
- timeout/network failure

## 401 Handling
- On 401, clear auth session coherently.
- Do not leave stale user state active.
- Redirect behavior may be handled centrally or by auth store/router integration, but it must be deterministic.

## Error Messaging
- Prefer backend `detail` when useful.
- Preserve arrays of validation issues meaningfully.
- Do not reduce all domain conflicts to generic transport text.

## Request Conventions by Operation Type

### Reads
- tolerate empty results
- surface unreachable backend clearly
- avoid duplicated loading logic patterns where composables can help

### Critical Mutations
- disable repeat submit while in flight
- surface 409 clearly
- surface 422 clearly
- avoid optimistic mutation of local state before backend success unless intentionally designed and reversible

## Pagination Conventions
- list endpoints that may grow should accept `skip` and `limit` patterns where backend supports them
- UI modules should be prepared for paginated purchase/history-style endpoints

## AI Agent Rules
- Do not create multiple competing API clients.
- Do not parse backend errors differently in every page.
- Do not scatter auth session clearing across many views if a central transport/auth layer can own it.