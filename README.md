# Spec-Driven Agentic Engineering

**A complete, runnable reference for directing AI coding agents from specification through verified implementation.**

This repository pairs an approval-workflow application with its feature
specification, architecture decisions, requirement-to-test traceability,
agent instructions, CI quality gates and an intentionally defective-change
demonstration. The companion handbook explains the engineering method; the
installed skill applies it to future repositories.

Read the handbook as [PDF](handbook/handbook.pdf), [offline HTML](handbook/handbook.html), or [editable Markdown](docs/handbook.md). The portable [companion agent skill](skills/spec-driven-agentic-engineering/SKILL.md) and its [installation instructions](skills/spec-driven-agentic-engineering/INSTALL.md) are included in full.

> Tested reference baseline, October 16, 2026: **31 passing automated tests**.
> `python scripts/acceptance_demo.py` confirms that a real maker-checker bypass
> is rejected by the same verification command used for valid code.

## Project contents

| Area | Contents |
| --- | --- |
| [`handbook/`](handbook/) | Printable PDF and fully offline HTML handbook |
| [`docs/`](docs/) | Source handbook, architecture decisions, diagrams, and six hands-on labs |
| [`reviewflow/`](reviewflow/) | Runnable FastAPI + SQLite request-approval example |
| [`specs/`](specs/) | Feature requirements and traceability |
| [`tests/`](tests/) | Acceptance, authorization, audit, and regression tests |
| [`skills/`](skills/) | Portable agent skill with templates, references, scripts, and evaluations |
| [`.agents/skills/`](.agents/skills/) | Installed skill for Codex |
| [`.claude/skills/`](.claude/skills/) | Installed skill for Claude Code |

All content is extracted source files. No ZIP extraction is required after cloning this repository.

## What you can do here

- Browse a local review-request application and try an approval as different users.
- Read an accepted specification and the architecture decisions behind it.
- Trace a requirement (such as REQ-014) through code and regression tests.
- Change a requirement and have Codex or Claude Code plan, implement and verify it.
- Run a two-sided acceptance demonstration: known-good accepted, known-defective blocked.
- Copy the included skill to other repositories.

## Start in five minutes

Requirements: **Python 3.11+**, pip and Git. No Docker, cloud service or model API is
required to execute the reference app or its tests.

### Linux, macOS or WSL

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -e '.[dev]'
python scripts/verify.py
python scripts/acceptance_demo.py
REVIEWFLOW_DEMO_MODE=1 python -m reviewflow
```

### Windows PowerShell

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
python scripts/verify.py
python scripts/acceptance_demo.py
$env:REVIEWFLOW_DEMO_MODE = "1"
python -m reviewflow
```

Open **http://127.0.0.1:8000**. Select Alice, submit a request, then switch to Bob
and approve it. Switch to Eve to demonstrate the dual-role maker-checker check:
Eve may create requests and review other users' requests, but cannot decide
her own.

The demo uses visible fixed tokens by design. It binds to loopback only and
fails startup without explicit demo mode or a supplied real resolver. **Never
expose this demo on a network or deploy it as a production authentication system.**

## Architecture at a glance

```text
 Browser (local demo)      HTTP API (FastAPI)
        |                         |
        +----------> authenticated identity resolver
                                  |
                           ReviewService
                    roles | maker-checker | state
                                  |
                            SQLite database
                           requests + audit

 Feature spec -> traceability -> executable tests -> verify.py -> CI
                                          |
                       acceptance_demo.py injects an actual defect
                       and proves the same gate refuses it
```

The example favors an inspectable, transactional vertical slice over a
complex deployment scaffold. See [architecture](docs/architecture.md) and
[ADR-0001](docs/decisions/0001-transactional-sqlite.md) for the tradeoffs.

## Verification commands

| Command | What it proves |
| --- | --- |
| `python scripts/spec_lint.py` | Spec IDs, task references, test functions and test markers agree |
| `python scripts/check_skills.py` | Skill files validate and Codex/Claude copies are identical |
| `python scripts/verify.py` | All static gates and runtime pytest suite pass |
| `python scripts/acceptance_demo.py` | Baseline passes; injected authorization bypass is caught |
| `python scripts/acceptance_demo.py --report evidence/run.json` | Same as above, with machine-readable evidence |

The static linter validates mappings, not behavioral semantics. Behavioral
requirements are checked by actual tests. The defect demonstration proves one
specific vulnerability is caught, not that the app is comprehensively secure.

## Evidence and traceability

- [Feature specification](specs/features/approval-workflow.md)
- [Requirement-test matrix](specs/traceability.json)
- [Execution plan](tasks/approval-workflow.md)
- [Local acceptance evidence](evidence/local-acceptance.json)
- [API and state design](docs/architecture.md)
- [PR verification workflow](.github/workflows/ci.yml)

**Follow REQ-014:** the spec prohibits self-approval, the service includes a
maker-checker guard, `test_requester_cannot_approve_own_request` verifies it,
and the acceptance script deliberately bypasses the guard in an isolated copy
to demonstrate the gate failing.

## Labs

Work through [the six guided labs](docs/labs/README.md): review a requirement,
plan a slice, extend behavior, coordinate independent tasks, inspect gate
sensitivity and make a requirement change. Lab 6 is an exercise; the two-level
approval feature is intentionally not implemented in the reference baseline.

## Agent setup

- Codex loads `.agents/skills/spec-driven-agentic-engineering/SKILL.md`.
- Claude Code loads `.claude/skills/spec-driven-agentic-engineering/SKILL.md`.
- `AGENTS.md` holds the shared project rules. `CLAUDE.md` points to them.
- `scripts/check_skills.py` catches divergence between the two installed copies.

Ask your coding agent:

> Read AGENTS.md and the spec-driven-agentic-engineering skill. Inspect
> REQ-014 in the specification, its task plan and its tests. Propose one small
> improvement with explicit acceptance criteria and no changes outside the
> authorized files. Do not code until the scope and tests are clear.

See the companion skill's `INSTALL.md` for copying it into other repositories.

## Local API example

```sh
# With REVIEWFLOW_DEMO_MODE=1 and the server running:
curl -sS -X POST http://127.0.0.1:8000/api/requests \
  -H 'Authorization: Bearer alice-local-demo' \
  -H 'Content-Type: application/json' \
  -d '{"title":"Replace old projector","description":"Room display fails during meetings"}'

# Open the interactive API documentation at http://127.0.0.1:8000/docs
```

## Project tree

```text
reviewflow/       FastAPI routes, domain policy, SQLite schema and demo UI
tests/            Requirement-tagged runtime regression tests
specs/            Accepted feature spec and machine-readable traceability
tasks/            Dependency-aware implementation work
docs/             Architecture, ADRs and six practical labs
scripts/          Verification, mutation acceptance and skill checks
.agents/skills/   Codex project skill
.claude/skills/   Identical Claude Code project skill
.github/          CI workflow and PR review template
AGENTS.md         Shared working conventions
CLAUDE.md         Claude-specific entrypoint
```

## Using this project as a template

Use `git clone <remote>` once you publish it. If you received the companion
Git bundle, **you can clone locally without a GitHub remote**:

```sh
git clone /path/to/spec-driven-agentic-engineering.bundle my-spec-project
cd my-spec-project
python -m pip install -e '.[dev]'
python scripts/verify.py
```

To publish your own clone, create an empty GitHub repository, then run
`git remote set-url origin <your-repository-url>` (for a bundle clone), then
`git push -u origin main`. For an unpacked ZIP initialized with `git init`, use
`git remote add origin <your-repository-url>` instead.
No remote was created as part of this deliverable.

To adapt the reference, keep the specification and traceability process,
replace the sample domain, and review the security limitations before reuse.

## Security and limitations

The `alice-local-demo`/`bob-local-demo` tokens are training credentials, not
secrets. The example does **not** ship a production identity provider, role
provisioning, TLS, rate limiting, request-level DDoS controls, centralized
audit retention, migrations, monitoring, backups or formal security assessment.
Approval semantics, visibility and database atomicity are genuinely enforced
within the reference's intended local scope.

## Sources and license

See the companion handbook's Source Notes for up-to-date upstream guidance on
Spec Kit, OpenSpec, Codex/Claude skills and OWASP agent security. Source code
and authored templates in this package are MIT licensed; third-party tools and
libraries keep their own licenses.
