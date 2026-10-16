# Install the spec-driven agentic engineering skill

Portable Agent Skills manifest: `SKILL.md`. No account, cloud service, remote
execution or MCP server is required to use the instructional material.

## Project installation

- Codex: copy the entire `spec-driven-agentic-engineering/` directory to
  `<repository>/.agents/skills/spec-driven-agentic-engineering/`.
- Claude Code: copy it to
  `<repository>/.claude/skills/spec-driven-agentic-engineering/`.
- To use both, put identical copies in both locations and track updates.

Both tools load project skills from these conventional paths (as of 2026-10-16).
The reference repository already includes both copies.

## Personal installation

For Codex: `~/.agents/skills/spec-driven-agentic-engineering/`.
For Claude Code: `~/.claude/skills/spec-driven-agentic-engineering/`.

## Validate

```sh
python scripts/validate_skill.py
```

Run the command from inside this skill folder. The built-in validator checks
packaging and eval metadata only. To evaluate agent behavior, present each
prompt in `evals/cases.json` to your intended agent and score the outputs
using `evals/scoring.md`. Do not report the static validation as a model eval.

## Create initial artifacts in an existing Git repository

```sh
python scripts/scaffold.py /path/to/your-repository
```

This creates template files only if absent; it never overwrites existing files.
Edit the placeholders before use. The skill does not modify repository settings.

## Relevant specifications

- https://agentskills.io/specification
- https://learn.chatgpt.com/docs/build-skills
- https://code.claude.com/docs/en/skills
