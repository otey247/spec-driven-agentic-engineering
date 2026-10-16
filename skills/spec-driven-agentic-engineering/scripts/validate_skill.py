#!/usr/bin/env python3
"""Dependency-free structural validation of this Agent Skills package.

Does NOT execute the model scenarios; see evals/cases.json for manual scoring.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

SKILL = Path(__file__).resolve().parents[1]
NAME = "spec-driven-agentic-engineering"


def validate(root: Path = SKILL) -> list[str]:
    issues: list[str] = []
    manifest = root / "SKILL.md"
    if not manifest.is_file():
        return ["SKILL.md missing"]
    body = manifest.read_text(encoding="utf-8")
    pieces = body.split("---", 2)
    if len(pieces) < 3 or pieces[0] != "":
        issues.append("Missing YAML frontmatter")
    else:
        fm = pieces[1]
        for key in ("name", "description"):
            if not re.search(rf"(?m)^{key}: \S", fm):
                issues.append(f"Missing required frontmatter {key}")
        if f"name: {NAME}" not in fm:
            issues.append("Skill name must match containing folder")
    if root.name != NAME:
        issues.append("Directory must match name")
    if len(body.splitlines()) > 500:
        issues.append("SKILL.md exceeds recommended 500 lines")
    files = re.findall(r"(?:references|assets|evals|scripts)/[\w.-]+", body)
    for reference in set(files):
        if not (root / reference).is_file():
            issues.append(f"Referenced skill asset missing: {reference}")
    for directory in ("references", "assets", "evals", "scripts"):
        if not (root / directory).is_dir():
            issues.append(f"Missing skill directory: {directory}")
    try:
        cases = json.loads((root / "evals/cases.json").read_text(encoding="utf-8"))
        names: set[str] = set()
        if len(cases["cases"]) < 10:
            issues.append("Expected at least 10 behavioral evaluation cases")
        for case in cases["cases"]:
            for key in ("id", "prompt", "expected", "must_not"):
                if not case.get(key):
                    issues.append(f"Missing eval field {key}: {case}")
            if case["id"] in names:
                issues.append(f"Duplicate eval id: {case['id']}")
            names.add(case["id"])
    except (OSError, KeyError, ValueError, TypeError) as e:
        issues.append(f"Invalid eval cases: {e}")
    return issues


if __name__ == "__main__":
    errors = validate()
    if errors:
        for issue in errors:
            print("FAIL:", issue)
        sys.exit(1)
    print("SKILL PACKAGE: PASS (format, reference paths and static eval manifest)")
    print("Note: behavioral eval scenarios require execution in a coding agent.")
