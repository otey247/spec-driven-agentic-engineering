#!/usr/bin/env python3
"""Single verification entrypoint shared by local development and CI."""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    checks = [
        ("Specification and traceability", [sys.executable, "scripts/spec_lint.py"]),
        ("Embedded agent skill", [sys.executable, "scripts/check_skills.py"]),
        ("Automated application tests", [sys.executable, "-m", "pytest", "-q"]),
    ]
    for title, command in checks:
        print(f"\n>>> {title}", flush=True)
        result = subprocess.run(command, cwd=ROOT, check=False)
        if result.returncode != 0:
            print(f"VERIFICATION: BLOCKED ({title})", flush=True)
            return result.returncode
    print("\nVERIFICATION: PASSED", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
