#!/usr/bin/env python3
"""Prove the quality gate accepts valid code and blocks a known introduced defect.

Works in temporary copies and never mutates the original checkout.
The defect is an intentional bypass of the maker-checker guard, not a mock.
"""
from __future__ import annotations

import argparse
import json
import platform
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = 'if actor.user_id == record["created_by"]:  # MAKER_CHECKER_GUARD'
INJECTED = 'if False and actor.user_id == record["created_by"]:  # MAKER_CHECKER_GUARD'
EXPECTED_TEST = "test_requester_cannot_approve_own_request"


def ignore(_directory, filenames):
    return {name for name in filenames if name in {".git", ".venv", "__pycache__", ".pytest_cache", ".data", "*.egg-info"} or name.endswith(".egg-info")}


def run_verify(directory: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "scripts/verify.py"], cwd=directory,
        text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False,
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, help="Write a machine-readable verification report")
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix="spec-driven-gate-") as scratch:
        tmp = Path(scratch)
        valid = tmp / "valid"
        defect = tmp / "defective"
        shutil.copytree(ROOT, valid, ignore=ignore)
        shutil.copytree(ROOT, defect, ignore=ignore)

        print("[1/2] Running all verification checks against a valid copy...", flush=True)
        accepted = run_verify(valid)
        if accepted.returncode != 0:
            print(accepted.stdout[-8000:])
            print("ACCEPTANCE: FAIL (baseline was not valid)")
            return 2
        print("BASELINE: PASS", flush=True)

        file = defect / "reviewflow" / "service.py"
        code = file.read_text(encoding="utf-8")
        if code.count(SOURCE) != 1:
            print("ACCEPTANCE: FAIL (expected guard location was not unique)")
            return 3
        file.write_text(code.replace(SOURCE, INJECTED), encoding="utf-8")
        print("[2/2] Introducing a real maker-checker bypass, then running the same checks...", flush=True)
        blocked = run_verify(defect)
        targeted_failure = blocked.returncode != 0 and EXPECTED_TEST in blocked.stdout and "FAILED" in blocked.stdout
        print("DEFECTIVE BUILD:", "BLOCKED" if targeted_failure else "UNEXPECTED RESULT", flush=True)
        if not targeted_failure:
            print(blocked.stdout[-9000:])
            return 4
        proof = {
            "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "python": platform.python_version(),
            "baseline": {"verification_command": "python scripts/verify.py", "passed": True, "return_code": accepted.returncode},
            "injected_defect": {
                "file": "reviewflow/service.py", "change": "Bypass creator identity check",
                "expected_failing_test": EXPECTED_TEST, "blocked": True,
                "verification_return_code": blocked.returncode,
            },
            "limitation": "Proves one selected known defect is caught, not comprehensive security coverage",
        }
        if args.report:
            args.report.parent.mkdir(parents=True, exist_ok=True)
            args.report.write_text(json.dumps(proof, indent=2) + "\n", encoding="utf-8")
            print(f"Report: {args.report}")
        print("ACCEPTANCE: PASS (valid change accepted; defective change rejected)")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
