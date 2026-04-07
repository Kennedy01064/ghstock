# AI Frontend UI/API Invariants

## Purpose
This file defines the invariants the SPA must preserve when consuming the backend.

AI agents must treat these rules as more important than UI convenience.

## Global Principles
- The backend is authoritative.
- The SPA must reflect backend truth, not invent a parallel truth.
- UI state must not imply a workflow transition that the backend has not confirmed.
- Session state must be internally coherent after login, logout, expiry, or 401.
- Role restrictions must be visible both in UX and route behavior.

## Session Invariants
- If there is no valid token, protected routes must not render as authenticated.
- If `/auth/me` fails after bootstrap, the session must be cleared coherently.
- Auth session persistence must not leave stale user info after logout or 401.
- Remember-session behavior must be explicit and deterministic.

## Router Invariants
- Guest-only routes must redirect authenticated users away.
- Protected routes must redirect unauthenticated users to login.
- Role-sensitive destinations must not rely only on menu hiding.
- Direct navigation to screens outside the user’s role scope should be blocked or redirected coherently.

## API Interaction Invariants
- All requests must go through shared transport handling.
- Backend status codes must remain distinguishable in the UI layer:
  - 401 unauthorized
  - 403 forbidden
  - 404 missing
  - 409 conflict
  - 422 validation/domain input issue
- The SPA must not reinterpret a conflict as success.

## Module Invariants

### Orders
- Draft/submitted/dispatched/delivered/cancelled states shown by UI must come from backend truth.
- The UI must not assume an order can transition just because a button is visible.
- Duplicate submit/reopen/cancel actions must be prevented while the request is in flight.

### Dispatch
- Pending/history/batch detail UI must not assume stock availability without backend confirmation.
- Confirmation/rejection actions must handle backend conflicts explicitly.
- Picking/export screens must reflect actual batch content from backend responses.

### Inventory
- UI must never silently “fix” insufficient inventory by clamping requested quantities.
- Inventory history shown to building admins must not expose other buildings’ data.
- Adjust/consume/transfer/return/shrinkage screens must treat backend conflicts as first-class UX outcomes.

### Purchases
- Purchase creation UI must not assume partial success.
- Purchase lists should not assume the backend returns the full dataset forever.
- UI should tolerate pagination or future pagination expansion.

### Catalog / Imports
- Import preview and commit must remain clearly separated.
- UI must not imply a commit occurred during preview.
- Product matching ambiguity should be surfaced, not hidden.

## Build / Environment Invariants
- Tailwind scanning must point to actual SPA source files.
- Vite config must reflect actual project structure.
- API base URL must be environment-driven and explicit.
- Frontend startup must not depend on implicit local-only behavior.

## What AI Agents Must Never Do
- Never recreate stock logic in the SPA.
- Never fake role permissions based only on visible menus.
- Never handle backend 409/422 as generic “unknown error” if better context is available.
- Never leave stale auth state after token invalidation.
- Never reintroduce build config that points to deleted legacy frontends.