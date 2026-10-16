# Start here

This repository contains the full extracted **Spec-Driven Agentic Engineering** learning package.

## Read the handbook

- [Printable PDF](handbook/handbook.pdf)
- [Offline HTML](handbook/handbook.html)
- [Editable Markdown source](docs/handbook.md)

## Run the reference application

Prerequisites: Python 3.11+ and Git. From the repository root:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/verify.py
python scripts/acceptance_demo.py
REVIEWFLOW_DEMO_MODE=1 python -m reviewflow
```

For Windows PowerShell, see the [README](README.md). Open http://127.0.0.1:8000. Do not deploy the demonstration tokens and identity resolver to production.

## Install the skill elsewhere

Copy [`skills/spec-driven-agentic-engineering/`](skills/spec-driven-agentic-engineering/) into `.agents/skills/` (Codex) or `.claude/skills/` (Claude Code) in another repository. The skill is already installed in both locations in this repository.

Run the validator:

```sh
python skills/spec-driven-agentic-engineering/scripts/validate_skill.py
```

The validator checks static formatting and supporting files. It does not run model-behavior evaluations.
