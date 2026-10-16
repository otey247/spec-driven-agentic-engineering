#!/usr/bin/env python3
"""Copy starter artifact templates into a target repo without overwriting files."""
from __future__ import annotations

import argparse
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = {
    "spec-template.md": "specs/features/new-feature.md",
    "plan-template.md": "tasks/new-feature.md",
    "adr-template.md": "docs/decisions/new-decision.md",
    "task-template.md": "tasks/new-task.md",
    "verification-report-template.md": "evidence/new-verification.md",
}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("target", type=Path, help="Existing target repository directory")
    args = parser.parse_args()
    target = args.target.resolve()
    if not target.is_dir() or not (target / ".git").exists():
        parser.error("Target must be an existing Git repository (a .git entry is required)")
    for source, destination in ARTIFACTS.items():
        dst = target / destination
        if dst.exists():
            print(f"SKIP {destination} (already exists)")
            continue
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / "assets" / source, dst)
        print(f"CREATE {destination}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
