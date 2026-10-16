# Six hands-on labs

**Prerequisite:** install dependencies and confirm `python scripts/verify.py`
passes before making changes. Each lab is based on the same request-approval
example. A coding agent is optional: the repository works without model access.

| Lab | Focus | Time target | Outcome |
| --- | --- | --- | --- |
| [01](01-from-problem-to-spec.md) | Problem, user goal, acceptance | 20 min | Revised specification proposal |
| [02](02-architecture-and-plan.md) | Architecture, ADRs, task boundaries | 25 min | Decision and bounded plan |
| [03](03-vertical-slice.md) | Test-first implementation | 35 min | New request behavior with tests |
| [04](04-multi-agent.md) | Parallel ownership and integration | 30 min | Reviewed handoffs and merge plan |
| [05](05-acceptance-gate.md) | Prove defective code is blocked | 15 min | Mutation acceptance evidence |
| [06](06-change-existing-feature.md) | Change the approval policy | 45 min | New spec and implementation proposal |

The reference baseline implements one-level approval. Lab 6's two-level
approval is intentionally **not implemented**, so there is meaningful work
to specify and build. Validate after every lab and do not treat an agent's
summary as a substitute for observed test results.
