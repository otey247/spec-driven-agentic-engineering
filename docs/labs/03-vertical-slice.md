# Lab 03: Implement a bounded vertical slice

## Do

1. Confirm baseline with `python scripts/verify.py`.
2. Choose the cancellation requirement from Lab 01 and obtain the intended
   approval/rejection semantics from the spec.
3. Add a requirement-tagged regression test before the new API handler.
4. Implement cancellation inside the trusted service with transactional state
   change and an audit event. Add its API route.
5. Update `schema.sql` action constraints, the traceability JSON and tasks.
6. Run `python scripts/verify.py`; capture real results in a handoff report.

## Agent prompt

> Implement only the accepted REQ-017 cancellation slice. Change the spec,
> traceability and tests together. Server-side rules must prevent cancellation
> of terminal requests. Keep creation and decision behavior unchanged. Run the
> full verification command, and report every failing test without hiding it.

## Done when

An authorized cancellation succeeds once, unauthorized and terminal requests
are rejected, audit records match state, and the regression suite passes.

**No solution is included:** this is an exercise beyond the baseline.
