# Lab 05: Show that the gate rejects a defect

## Do

```sh
python scripts/verify.py
python scripts/acceptance_demo.py --report evidence/lab05.json
```

The second command makes two temporary repository copies. The baseline copy
must pass. In the other copy, the script bypasses the maker-checker guard in
`reviewflow/service.py` and runs the same verifier. The exercise succeeds only
when the targeted test fails and the verifier exits nonzero.

## Inspect

- Which requirement and test caught the defect?
- Why is a role check alone insufficient for a dual-role creator?
- Why would an agent-generated report saying "looks correct" be inadequate?
- What does this demonstration **not** prove about application security?

## Done when

The command reports `ACCEPTANCE: PASS (valid change accepted; defective change
rejected)` and includes both observed outcomes in the JSON report.
