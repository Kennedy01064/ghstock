# AI Frontend Phase 4 — Resilience and UX States

## Phase Goal
Make the SPA safe and clear under slow network, backend conflicts, retries, and partial data conditions.

## In Scope
- loading states
- retry-safe UX
- disabled states for critical buttons
- empty states
- conflict messages
- validation feedback
- list/query behavior under larger datasets

## Out of Scope
- visual branding overhaul
- backend redesign

## Current Problems This Phase Must Solve
- operational screens tend to become fragile when backend latency increases
- duplicate submit behavior often comes from missing in-flight lock patterns
- conflict and validation states can be underexplained to the user
- list screens must tolerate pagination growth and partial fetch states

## Concrete Tasks

### 1. Add In-Flight Safety
- disable critical mutation actions while request is pending
- avoid duplicate intent from double click
- preserve ability to retry after failure

Acceptance:
- critical mutations are not trivially duplicated by UI behavior

### 2. Improve Error-State UX
- distinguish forbidden vs conflict vs validation vs unreachable backend
- show conflict-specific guidance where possible

Acceptance:
- operators understand what happened and what to do next

### 3. Harden List and Detail Views
- coherent loading states
- empty states
- error states
- support for paginated growth where backend now paginates

Acceptance:
- data-heavy modules behave predictably under normal operational load

### 4. Review Slow-Network UX
- ensure screens do not appear frozen without feedback
- keep request lifecycle visible for critical operations

Acceptance:
- SPA remains understandable under latency