# AI Frontend Phase 1 — Foundation and Auth

## Phase Goal
Stabilize app bootstrap, auth lifecycle, route protection, and build correctness.

## In Scope
- review `main.js` bootstrap
- auth store initialization behavior
- guest-only vs auth-required navigation
- role-aware post-login landing logic
- build correctness in Vite/Tailwind configuration
- remove legacy frontend build assumptions

## Out of Scope
- broad visual redesign
- full API client rewrite
- module-specific workflow refactors

## Current Problems This Phase Must Solve
- route guard is token-based but not role-aware enough
- auth session is stored in browser storage and must remain coherent after expiry
- Vite config is minimal and Tailwind config still points to legacy frontend paths
- app bootstrap depends on auth initialization but that flow should stay predictable and cheap

## Concrete Tasks

### 1. Harden Auth Bootstrap
- review `initialize()`
- ensure stale token + failed `/auth/me` always clears session coherently
- avoid ambiguous partial-auth UI state

Acceptance:
- refresh with stale token lands in a clean unauthenticated state

### 2. Harden Route Guards
- preserve guest-only/login behavior
- protect auth-required areas
- add role-aware route protection where clearly needed
- do not rely only on hidden navigation links

Acceptance:
- direct URL navigation respects auth and role expectations

### 3. Make Role Redirects Deterministic
- post-login route should be role-aware
- already-authenticated users opening `/login` should redirect consistently
- home/dashboard routing should not depend on stale user assumptions

Acceptance:
- dashboard landing is deterministic for each role

### 4. Fix Build Foundations
- align `tailwind.config.js` with `frontend-spa/src/**/*.{vue,js}`
- verify Vite config reflects actual SPA structure
- document required frontend env vars

Acceptance:
- build tooling matches the real SPA, not the removed legacy frontend

## Definition of Done
- auth bootstrap is coherent
- route guarding is stronger
- role landing is deterministic
- build config is aligned with the SPA