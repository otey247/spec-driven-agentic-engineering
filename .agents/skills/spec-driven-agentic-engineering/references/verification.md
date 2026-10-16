# Verification and traceability reference

## Build evidence from observable tests

Use stable requirement IDs and link each to at least one verifiable behavior.
A matrix row should contain ID, scenario, implementation location, test command,
observed result and reviewer. Do not assume a test file exists because a plan
mentions it. Resolve the actual executable test identifier.

For risk-sensitive behavior add negative tests: authorization denied, expired
credential, double submission, race conditions, partial failure, forbidden
side effects, replay, missing data, and malformed inputs.

## Verify different properties at the right level

- Unit: domain rules, state transitions, pure functions.
- API/integration: persistence, permissions, transactionality, interface contracts.
- End-to-end: complete user tasks, accessibility behavior, real browser interactions.
- Security: negative authorization paths, secrets and dependency checks, isolation.
- Performance/reliability: load assumptions, concurrency, failure and recovery.
- Agentic execution: evaluation datasets, tool-call outcomes, grounding, replay,
  policy, scope limits and incomplete workflow handling.

## Acceptance commands

Use one shared verification entrypoint across local engineering and CI. A
pipeline must fail when a required check fails. Prefer machine-readable test
reports and stable exit codes. Run the command in a clean environment before
claiming a change is done.

Demonstrate that high-value gates reject deliberately incorrect behavior.
Example: inject a test fixture or code mutation that bypasses a maker-checker
rule; run the *same* release verification command; require non-zero exit status
and identify the intended test failure. This demonstrates selected gate
sensitivity. It does not prove exhaustive coverage.

## Review report contents

1. Change scope and linked requirements.
2. Test commands actually executed (environment and timestamp).
3. Pass, fail, skipped and blocked checks.
4. Unverified assumptions and remaining risks.
5. Required approval and release decision.

Never mark an unexecuted gate "passed." A code-review comment, lint result or
agent summary is not interchangeable with runtime verification.
