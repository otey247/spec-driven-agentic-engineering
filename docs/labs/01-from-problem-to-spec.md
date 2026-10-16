# Lab 01: From a user problem to a testable specification

## Scenario

An operations employee currently asks for equipment in chat. Management
approvals are inconsistent and requesters cannot tell what happened.

## Do

1. Read `specs/features/approval-workflow.md` and `specs/traceability.json`.
2. Identify users, state transitions, three failure cases, and the explicit
   out-of-scope items.
3. Review `REQ-014`: dual-role actors must not approve their own requests.
4. Draft an additional requirement for cancellation by the creator, but stop
   before implementing it. Specify the allowed states and audit behavior.
5. Propose acceptance tests, including a failed cancellation after approval.

## Agent prompt

> Read AGENTS.md and the spec-driven-agentic-engineering skill. Analyze the
> existing feature specification. Propose a scoped REQ-017 for requester
> cancellation of pending requests. Preserve existing approval authorization,
> make failure behavior testable, and do not change application code.

## Done when

You can show the difference between the existing behavior and proposed change;
all new scenarios have unambiguous observable outcomes and named verification.
