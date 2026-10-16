# Execution plan: approval workflow

Source: `specs/features/approval-workflow.md`  
Architecture: `docs/architecture.md`  
Status: Implemented reference baseline; retain plan to exercise future changes.

| Task | Requirements | Dependencies | Owner boundary | Completion evidence |
|---|---|---|---|---|
| TASK-001 Schema and audit data | REQ-002, REQ-016 | None | `reviewflow/schema.sql`, `reviewflow/service.py` | Create and audit tests pass |
| TASK-002 Authentication and roles | REQ-001, REQ-004, REQ-011 | None | `reviewflow/auth.py` | Auth rejection and fail-closed tests pass |
| TASK-003 Create and read API | REQ-002, REQ-003, REQ-005, REQ-010, REQ-012 | TASK-001, TASK-002 | `reviewflow/api.py` | Request and visibility tests pass |
| TASK-004 Decision state machine | REQ-006, REQ-007, REQ-008, REQ-014 | TASK-001, TASK-002 | `reviewflow/service.py` | Approval and maker-checker tests pass |
| TASK-005 Atomic updates | REQ-009, REQ-016 | TASK-004 | `reviewflow/service.py`, `tests/test_approvals.py` | Two concurrent decisions produce one commit |
| TASK-006 Convergence and release | REQ-013, REQ-001, REQ-002, REQ-003, REQ-004, REQ-005, REQ-006, REQ-007, REQ-008, REQ-009, REQ-010, REQ-011, REQ-012, REQ-014, REQ-016 | TASK-001..005 | repo-wide | Spec lint, tests, mutation acceptance command |

| TASK-007 Local demo interface | REQ-013 | TASK-003 | `reviewflow/static/index.html`, `reviewflow/api.py` | Demo page is opt-in and route is isolated |

## Handoff expectations

Every worker reports: task ID, requirement IDs, owned files, changes made,
actual test commands and results, open assumptions, and risks. A coordinator
integrates and reruns repo-wide verification after merges.

## Convergence rule

- Do not mark a task complete based only on an agent summary.
- Failed CI, absent requirement mappings or missing evidence block release.
- A discovered ambiguity updates the specification and plan before rework.
