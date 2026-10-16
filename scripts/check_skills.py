#!/usr/bin/env python3
"""Check both project skill copies are equivalent and structurally valid."""
from __future__ import annotations

import hashlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANON = ROOT / ".agents/skills/spec-driven-agentic-engineering"
MIRROR = ROOT / ".claude/skills/spec-driven-agentic-engineering"


def contents(directory: Path) -> dict[str, str]:
    return {str(path.relative_to(directory)): hashlib.sha256(path.read_bytes()).hexdigest()
            for path in directory.rglob("*") if path.is_file() and "__pycache__" not in path.parts}


def main() -> int:
    if not CANON.is_dir() or not MIRROR.is_dir():
        print("SKILL CHECK: FAIL (both project skill locations are required)")
        return 1
    if contents(CANON) != contents(MIRROR):
        print("SKILL CHECK: FAIL (Codex and Claude skill copies have drifted)")
        return 1
    result = subprocess.run([sys.executable, str(CANON / "scripts/validate_skill.py")], cwd=ROOT, check=False)
    if result.returncode != 0:
        return result.returncode
    print("SKILL CHECK: PASS (mirrored directories match)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
