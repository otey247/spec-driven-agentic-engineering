# Delivery workflow reference

The workflow is iterative. Discover new facts, amend the spec and keep evidence
connected. A specification does not create certainty where source material is
unclear.

## Starting from scratch

1. Problem framing: identify users, observed pain, desired behavior and measure
   of success. Output: one-page problem/scope statement.
2. Specification: write scenarios, policies, failure paths and measurable
   quality constraints. Output: numbered requirements and acceptance criteria.
3. Design: agree on interfaces, data ownership, trust boundaries, architecture,
   dependencies and deployments. Output: ADRs and contracts.
4. Plan: identify a thin vertical slice, implementation tasks, ownership and
   prerequisites. Output: dependency-aware executable task list.
5. Implement: code and tests, small commits/PRs, bounded agent scope. Output:
   working changes with provenance.
6. Verify: cross-check every in-scope requirement against test results and
   inspect the user experience. Output: traceability and observed evidence.
7. Converge: revise discrepancies, obtain approvals, release and update the
   canonical specification. Output: reviewed change record.

## Updating an existing product

First inspect code, API contracts, tests, schema, deployment and current UI.
Write an "as-is" behavior summary. Explicitly distinguish preserved behavior
from intended change. Test backwards compatibility, data migrations and any
old-to-new transition. Never rewrite the entire architecture as a prerequisite
to a bounded defect or feature.

## Match artifact depth to the change

- Small mechanical edit: issue description, applicable existing standards, a
  focused test or relevant verification. A full PRD is usually wasteful.
- Feature: scoped spec, acceptance criteria, task plan and direct tests.
- Cross-service or high-impact feature: architectural decisions, contracts,
  failure modes, rollout and rollback plan, dependency graph and review owners.
- High-risk/regulated change: add formal threat modeling, evidence retention,
  control mapping and named approval authority. Apply actual organizational
  requirements rather than claiming a generic universal compliance process.

## Entry and exit criteria

| Phase | Enter when | Exit when |
| --- | --- | --- |
| Discovery | User job/defect known | Outcome, scope, assumptions documented |
| Specification | Target outcome bounded | All critical scenarios have observable acceptance criteria |
| Design | Behavior and constraints understood | Interfaces and tradeoffs reviewed |
| Planning | Design boundaries stable enough | Tasks have ownership, prerequisites and verification |
| Execution | Task unblocked | Code and related tests changed, checks observed |
| Verification | Integrated code available | All required checks pass; gaps or waivers explicit |
| Release | Authority and checks satisfied | Deployment observed, rollback available, spec updated |

## Managing ambiguity

If missing information can be safely deferred, label an assumption, limit
scope and proceed with a reversible design. If it affects money, identity,
regulated data, destructive actions or irreversible migration, stop and obtain
a decision. Never convert an unverified inference into a requirement.

## Convergence review questions

- Does each implemented branch represent an accepted scenario?
- Are error cases and authorization enforced at the server boundary?
- Do test names and assertions actually prove the mapped acceptance criteria?
- Are old contracts and migrations accounted for?
- Has the integration branch been tested after merge?
- Do operational defaults fail safely?
- Is each gap explicit and owned?
