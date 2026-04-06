# AI Backend Master Execution Block

## Purpose
This is the single master instruction block for AI coding agents working on the backend.

Use this file as the primary execution prompt or as the top-level instruction document.
It enforces strict sequential work:
- no phase mixing
- no phase skipping
- no advancing to the next phase until the current phase is fully completed

## Mandatory Reading Order
Before doing any work, the AI agent must read and follow these files in this exact order:

1. `docs/AI_BACKEND_IMPLEMENTATION_RULES.md`
2. `docs/AI_BACKEND_DOMAIN_INVARIANTS.md`
3. `docs/AI_BACKEND_API_CONVENTIONS.md`
4. `docs/AI_BACKEND_ROADMAP.md`
5. the current phase file only

Current phase files:
- `docs/AI_BACKEND_PHASE_1_FOUNDATION.md`
- `docs/AI_BACKEND_PHASE_2_DATA_INTEGRITY.md`
- `docs/AI_BACKEND_PHASE_3_INVENTORY_ENGINE.md`
- future phases must follow the same pattern

## Global Execution Rules

### Rule 1 — Work One Phase at a Time
The AI agent may work on only one phase per implementation cycle.
It must not combine tasks from multiple phases in the same code change unless the current phase document explicitly says they are inseparable.

### Rule 2 — No Advancing Without Completion
The AI agent must not start the next phase if the current phase is not fully complete.
Completion means:
- all in-scope tasks for the current phase are implemented
- the current phase acceptance criteria are satisfied
- any migration or compatibility notes for the current phase are documented
- remaining open risks are listed explicitly

If the phase is incomplete, the AI agent must stop and report what remains.

### Rule 3 — No Silent Combination
The AI agent must not smuggle work from a later phase into the current phase “for convenience”.
Examples of forbidden behavior:
- adding reservation logic during Phase 1 if Phase 1 only covers foundation
- redesigning purchases during a data-integrity phase
- introducing mobile-auth redesign during inventory-engine work

### Rule 4 — Backend Only
Unless explicitly instructed otherwise, these execution blocks are backend-only.
The AI agent must not modify `frontend-spa` while executing backend phases.

### Rule 5 — Preserve Stability
Public API contracts should remain stable unless a change is strictly necessary for the current phase.
If a breaking change is unavoidable, it must be called out explicitly.

## Phase Gate Protocol
At the end of each phase implementation, the AI agent must produce a gate report with this structure:

```text
PHASE GATE REPORT
Phase: <phase number and name>
Status: COMPLETE or INCOMPLETE

Files changed:
- ...

Migrations added/updated:
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
```

### Hard Gate Rule
The AI agent may only set `Next phase allowed: YES` if all current-phase acceptance criteria are complete.
If any required item is incomplete, it must set `Next phase allowed: NO`.

## Approved Sequential Order
The backend must be implemented in this order only:

### Phase 1 — Foundation and Safety
File:
- `docs/AI_BACKEND_PHASE_1_FOUNDATION.md`

Allowed work:
- startup cleanup
- migration setup
- safer config/CORS handling
- service-layer foundation
- domain error normalization

Forbidden work:
- reservation engine
- partial dispatch
- returns/transfers/shrinkage
- major purchase redesign

### Phase 2 — Data Integrity and Invariants
File:
- `docs/AI_BACKEND_PHASE_2_DATA_INTEGRITY.md`

Allowed work:
- unique constraints
- invariant-protecting indexes
- quantity checks
- draft uniqueness hardening
- conflict detection strategy

Forbidden work:
- full stock reservation engine
- full ledger redesign
- advanced workflow redesign outside integrity needs

### Phase 3 — Inventory Engine and Stock Ledger
File:
- `docs/AI_BACKEND_PHASE_3_INVENTORY_ENGINE.md`

Allowed work:
- stock semantics clarification
- reservation/release mechanics
- audit-oriented movement design
- explicit building inventory consumption behavior
- adjustment semantics

Forbidden work:
- unrelated frontend changes
- broad auth redesign
- mixing future workflow/UI concerns without backend need

### Future Phases
Future execution must continue in the same strict pattern:
- one phase file
- one implementation scope
- one gate report
- no mixing

## Master Prompt Block for AI Coding Agents
Use the following block when instructing an AI coding tool:

```text
Read and follow these files in order:
1. docs/AI_BACKEND_IMPLEMENTATION_RULES.md
2. docs/AI_BACKEND_DOMAIN_INVARIANTS.md
3. docs/AI_BACKEND_API_CONVENTIONS.md
4. docs/AI_BACKEND_ROADMAP.md
5. <CURRENT_PHASE_FILE>

Execution rules:
- Work on backend only.
- Execute only the current phase.
- Do not combine with later phases.
- Do not skip ahead.
- Do not start the next phase if the current one is incomplete.
- If the current phase cannot be fully completed, stop and output a PHASE GATE REPORT with `Next phase allowed: NO`.
- Keep API contracts stable unless strictly necessary.
- Prefer small, coherent changes.
- Report files changed, migration impact, behavior changes, compatibility concerns, and open risks.

Now execute only: <CURRENT_PHASE_NAME>
```

## Recommended Usage Pattern
When running Antigravity or a similar tool, issue one prompt per phase.
Do not ask it to “implement everything”.
Instead:
1. run Phase 1 only
2. verify gate report
3. only then run Phase 2
4. verify gate report
5. only then run Phase 3

## What the AI Agent Must Do If It Encounters Incomplete Work
If it finds that the phase is too large or partially blocked, it must:
- continue only within the current phase scope
- finish as much of the current phase as possible
- stop before touching next-phase work
- emit an `INCOMPLETE` gate report
- explicitly state that next phase is not allowed yet

## What the AI Agent Must Never Do
- never merge multiple phases into one big refactor
- never implement future-phase logic “to save time”
- never move business logic into the SPA
- never weaken invariants for convenience
- never claim phase completion if acceptance criteria are not satisfied

## Final Instruction
This file is the execution governor.
If there is any conflict between convenience and phase discipline, phase discipline wins.
