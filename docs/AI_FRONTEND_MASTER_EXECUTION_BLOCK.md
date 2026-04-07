# AI Frontend Master Execution Block

## Purpose
This is the single master instruction block for AI coding agents working on `frontend-spa`.

Use this file as the primary execution prompt or as the top-level instruction document.
It enforces strict sequential work:
- no phase mixing
- no phase skipping
- no advancing to the next phase until the current phase is fully completed

## Mandatory Reading Order
Before doing any work, the AI agent must read and follow these files in this exact order:

1. `docs/AI_FRONTEND_IMPLEMENTATION_RULES.md`
2. `docs/AI_FRONTEND_UI_API_INVARIANTS.md`
3. `docs/AI_FRONTEND_API_CLIENT_CONVENTIONS.md`
4. `docs/AI_FRONTEND_ROADMAP.md`
5. the current phase file only

Current phase files:
- `docs/AI_FRONTEND_PHASE_1_FOUNDATION_AND_AUTH.md`
- `docs/AI_FRONTEND_PHASE_2_API_CLIENT_AND_ERROR_HANDLING.md`
- `docs/AI_FRONTEND_PHASE_3_OPERATIONAL_MODULES.md`
- `docs/AI_FRONTEND_PHASE_4_RESILIENCE_AND_UX_STATES.md`
- `docs/AI_FRONTEND_PHASE_5_MOBILE_READINESS_AND_CONTRACTS.md`

## Global Execution Rules

### Rule 1 — Work One Phase at a Time
The AI agent may work on only one phase per implementation cycle.
It must not combine tasks from multiple phases in the same code change unless the current phase document explicitly says they are inseparable.

### Rule 2 — No Advancing Without Completion
The AI agent must not start the next phase if the current phase is not fully complete.
Completion means:
- all in-scope tasks for the current phase are implemented
- the current phase acceptance criteria are satisfied
- any compatibility notes for the current phase are documented
- remaining open risks are listed explicitly

If the phase is incomplete, the AI agent must stop and report what remains.

### Rule 3 — No Silent Combination
The AI agent must not smuggle work from a later phase into the current phase “for convenience”.
Examples of forbidden behavior:
- redesigning every store during a client-error phase
- adding visual redesign during API contract work
- introducing mobile UX redesign during auth hardening

### Rule 4 — Frontend SPA Only
Unless explicitly instructed otherwise, these execution blocks are frontend-only.
The AI agent must not modify backend contracts unless explicitly allowed by a separate instruction.

### Rule 5 — Respect Backend Authority
The frontend must not recreate business-critical logic that belongs to FastAPI.
The SPA may:
- guide
- validate basic input shape
- prevent accidental duplicate submits
- display backend states clearly

The SPA must not:
- invent its own stock truth
- fake workflow transitions
- bypass backend errors with optimistic assumptions

## Phase Gate Protocol
At the end of each phase implementation, the AI agent must produce a gate report with this structure:

```text
PHASE GATE REPORT
Phase: <phase number and name>
Status: COMPLETE or INCOMPLETE

Files changed:
- ...

Behavior changes:
- ...

Acceptance criteria check:
- [x] criterion 1
- [x] criterion 2
- [ ] criterion 3

Compatibility impact:
- ...

Open risks:
- ...

Next phase allowed:
- YES or NO