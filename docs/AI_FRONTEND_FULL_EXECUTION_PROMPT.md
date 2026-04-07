# AI Frontend Full Sequential Execution Prompt

Copy and paste the following prompt into Antigravity or a similar AI coding tool.

```text
Read and follow these files strictly and in this exact order:

1. docs/AI_FRONTEND_MASTER_EXECUTION_BLOCK.md
2. docs/AI_FRONTEND_IMPLEMENTATION_RULES.md
3. docs/AI_FRONTEND_UI_API_INVARIANTS.md
4. docs/AI_FRONTEND_API_CLIENT_CONVENTIONS.md
5. docs/AI_FRONTEND_ROADMAP.md
6. docs/AI_FRONTEND_PHASE_1_FOUNDATION_AND_AUTH.md
7. docs/AI_FRONTEND_PHASE_2_API_CLIENT_AND_ERROR_HANDLING.md
8. docs/AI_FRONTEND_PHASE_3_OPERATIONAL_MODULES.md
9. docs/AI_FRONTEND_PHASE_4_RESILIENCE_AND_UX_STATES.md
10. docs/AI_FRONTEND_PHASE_5_MOBILE_READINESS_AND_CONTRACTS.md

Your mission:
Execute all frontend phases in sequence, from Phase 1 through Phase 5, but with these non-negotiable rules:

GLOBAL RULES
- Work on `frontend-spa` only.
- Do not modify backend unless explicitly required by a separate instruction.
- Do not combine phases.
- Do not skip phases.
- Do not start a new phase until the current phase is fully completed.
- If a phase is incomplete, stop immediately and do not continue to the next phase.
- Keep backend API contracts respected as they currently exist.
- Prefer small, coherent, reviewable commits.
- Respect the UI/API invariants and API client conventions from the docs.

PHASE EXECUTION RULES
For each phase:
1. Read the corresponding phase document again before making changes.
2. Implement only the work allowed in that phase.
3. Do not include work from later phases, even if it seems convenient.
4. When the phase is finished, output a PHASE GATE REPORT.
5. Only continue to the next phase if and only if the PHASE GATE REPORT says:
   - Status: COMPLETE
   - Next phase allowed: YES

PHASE GATE REPORT FORMAT
Use exactly this structure after every phase:

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

HARD STOP RULE
If any acceptance criterion for the current phase is not satisfied:
- mark Status: INCOMPLETE
- mark Next phase allowed: NO
- stop execution
- do not begin the next phase

PHASE ORDER
Execute in this exact order only:
1. Phase 1 — Foundation and Auth
2. Phase 2 — API Client and Error Handling
3. Phase 3 — Operational Modules
4. Phase 4 — Resilience and UX States
5. Phase 5 — Mobile Readiness and Contracts

QUALITY RULES
- Views compose; stores share state; composables reuse logic; API client handles transport.
- Do not recreate backend business rules in the SPA.
- Do not leave route protection based only on menu visibility.
- Do not swallow 409/422 conflicts into generic errors.
- Do not keep legacy build config pointing to removed frontend paths.
- Keep auth/session behavior coherent.
- Keep critical mutation UX safe against duplicate submits.

FINAL DELIVERY RULE
At the very end, if all phases are fully completed, output a final summary with:
1. all phases completed
2. files changed by phase
3. breaking changes or compatibility notes
4. remaining risks, if any

Now begin with Phase 1 only.
If Phase 1 is not fully complete, stop there.
If Phase 1 is complete, continue to Phase 2, and so on, always respecting the hard gate rule.