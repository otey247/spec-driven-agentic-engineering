#!/usr/bin/env python3
"""Check exact requirement -> test mapping without requiring test execution.

Passing this static check does not prove behavior. scripts/verify.py also runs pytest.
"""
from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ID_PATTERN = re.compile(r"^REQ-\d{3}$")


def test_marks(file: Path) -> dict[str, set[str]]:
    tree = ast.parse(file.read_text(encoding="utf-8"), filename=str(file))
    result: dict[str, set[str]] = {}
    for node in ast.walk(tree):
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) or not node.name.startswith("test_"):
            continue
        marks: set[str] = set()
        for decorator in node.decorator_list:
            if not isinstance(decorator, ast.Call) or not decorator.args:
                continue
            function = decorator.func
            if (
                isinstance(function, ast.Attribute)
                and function.attr == "requirement"
                and isinstance(function.value, ast.Attribute)
                and function.value.attr == "mark"
                and isinstance(function.value.value, ast.Name)
                and function.value.value.id == "pytest"
                and isinstance(decorator.args[0], ast.Constant)
                and isinstance(decorator.args[0].value, str)
            ):
                marks.add(decorator.args[0].value)
        result[node.name] = marks
    return result


def check(root: Path = ROOT) -> list[str]:
    problems: list[str] = []
    try:
        matrix = json.loads((root / "specs/traceability.json").read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        return [f"Cannot load traceability matrix: {error}"]
    try:
        spec = (root / matrix["spec"]).read_text(encoding="utf-8")
        tasks = (root / matrix["task_plan"]).read_text(encoding="utf-8")
    except (OSError, KeyError) as error:
        return [f"Missing feature spec or task plan: {error}"]
    seen: set[str] = set()
    marked: dict[Path, dict[str, set[str]]] = {}
    for req in matrix.get("requirements", []):
        identifier = req.get("id", "")
        if not ID_PATTERN.fullmatch(identifier):
            problems.append(f"Bad requirement ID: {identifier!r}")
        if identifier in seen:
            problems.append(f"Duplicate requirement ID: {identifier}")
        seen.add(identifier)
        if f"### {identifier}:" not in spec:
            problems.append(f"{identifier}: no labeled spec section")
        if identifier not in tasks:
            problems.append(f"{identifier}: missing from task plan")
        if not req.get("tests"):
            problems.append(f"{identifier}: no test mapping")
        for ref in req.get("tests", []):
            if "::" not in ref:
                problems.append(f"{identifier}: invalid test reference {ref}")
                continue
            relative_file, test_name = ref.split("::", 1)
            test_file = root / relative_file
            if not test_file.exists():
                problems.append(f"{identifier}: missing test file {relative_file}")
                continue
            if test_file not in marked:
                try:
                    marked[test_file] = test_marks(test_file)
                except (SyntaxError, OSError) as err:
                    problems.append(f"{relative_file}: cannot parse test: {err}")
                    continue
            if test_name not in marked[test_file]:
                problems.append(f"{identifier}: missing test function {ref}")
            elif identifier not in marked[test_file][test_name]:
                problems.append(f"{identifier}: test function lacks matching @pytest.mark.requirement: {ref}")
    documented = set(re.findall(r"^### (REQ-\d{3}):", spec, flags=re.MULTILINE))
    for missing in sorted(documented - seen):
        problems.append(f"{missing}: spec section has no traceability matrix entry")
    if not seen:
        problems.append("Traceability matrix is empty")
    for required in ("AGENTS.md", "docs/architecture.md", "docs/decisions/0001-transactional-sqlite.md"):
        if not (root / required).exists():
            problems.append(f"Required engineering document missing: {required}")
    return problems


if __name__ == "__main__":
    errors = check()
    if errors:
        print("SPEC TRACEABILITY: FAIL")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    print("SPEC TRACEABILITY: PASS (requirements, spec, tasks and test markers agree)")
