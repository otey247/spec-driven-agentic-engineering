# Lab 04: Coordinate multiple implementation agents

## Setup

Use Git worktrees for independent tasks when supported:

```sh
git worktree add -b lab/api ../lab-api main
git worktree add -b lab/ui ../lab-ui main
```

## Do

1. Assign a service/API task to Agent A and a UI task to Agent B.
2. Freeze the API contract before concurrent implementation begins.
3. Make each agent report changed files, actual test results and blocked work.
4. Have an integration owner review both contributions and reconcile conflicts.
5. Re-run all tests from the integrated branch, not only agent-owned tests.

## Agent prompt

> Act as the integration owner. Read the specification and agent handoffs,
> compare implemented contracts, identify overlapping edits, and create an
> integration checklist. Do not merge or overwrite work without authorization.

## Done when

An independent reviewer can reconstruct what each agent changed and which
checks were run after integration. Clean up worktrees only when their work is
merged or explicitly discarded.
