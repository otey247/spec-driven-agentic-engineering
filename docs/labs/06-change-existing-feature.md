# Lab 06: Evolve the system to two-level approval

## Scenario

Requests above a specified financial threshold now require two approvals from
**two different approvers**. A person may not approve their own request or
satisfy both approval levels. Requests below the threshold keep one-level
approval. Avoid inventing the threshold or currency; have a human owner supply
it before committing to behavior.

## Do

1. Inspect current state, database schema and external API response contract.
2. Write a change specification that preserves one-level behavior for existing
   eligible requests and clarifies migration of pending requests.
3. Specify two distinct approver identities, audit records, collision behavior,
   rejection and rollback semantics.
4. Add contract and concurrency tests before changing the schema.
5. Produce ADR(s) for changed authoritative state; implement incrementally.
6. Run existing tests and new requirement tests in CI.

## Agent prompt

> Propose a production-oriented change specification and design for conditional
> two-level approval. Inspect the current repo first. Do not invent the spend
> threshold or authorization roles. Preserve old client contracts where
> possible. Include migrations, transaction boundaries, concurrent approvals,
> audit, negative tests, human approvals and rollback. Stop before production
> schema or deployment actions.

## Done when

You have a reviewed proposal, bounded tasks, updated tests and a clear
acceptance gate; if you implement, ensure all checks actually pass. Do not
claim the baseline code already supports two levels.
