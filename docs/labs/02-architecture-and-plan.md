# Lab 02: Architecture and executable task planning

## Do

1. Inspect `docs/architecture.md`, the accepted ADR and `tasks/approval-workflow.md`.
2. Draw the trust boundary separating browser, API, identity and domain service.
3. Explain why status and audit changes use one transaction.
4. Turn proposed REQ-017 from Lab 01 into two or three independent tasks with
   prerequisites, permitted paths and verification commands.
5. Identify which tasks could run in parallel and which cannot.

## Agent prompt

> Review proposed REQ-017 with AGENTS.md and the installed skill. Produce an
> ADR only if an architectural decision is required. Plan a vertical slice,
> identify contract boundaries, assign test ownership, and include precise
> dependency and merge rules. Do not make code changes yet.

## Done when

Every task can be accepted with a concrete check; no task relies on a hidden
handoff or ambiguous authorization decision.
