# Additional contracts when the product contains runtime agents

A coding agent may implement ordinary application code. A product that runs
agent workflows also needs runtime authority, state, tool and evaluation design.

| Contract | Define | Acceptance example |
| --- | --- | --- |
| Agent role | Objective, limits, inputs and outputs | Agent stops on out-of-scope request |
| Tools | Schemas, identity, permissions, failures, idempotency | Tool rejects unauthorized caller even if model requests action |
| Orchestration | Deterministic states, allowed model decisions, loops, timeouts | Failed tool resumes at checkpoint without duplicate side effects |
| Authority | Autonomous, human-approved and forbidden actions | Payment tool waits for explicit human authorization |
| State | Durable canonical state and events, replay strategy | Crash recovery resumes without re-applying a write |
| Knowledge | Sources, freshness, citations, retrieval boundaries | Missing evidence leads to refusal or escalation |
| Evaluation | Tasks, scenarios, gold outcomes, statistical checks | Defective/replayed tool outcome is caught |
| Observability | Trace IDs, tool calls, decisions, cost, approval, redaction | Investigator can reconstruct an action chain |

## Orchestration choices

Prefer deterministic orchestration for identity, transaction boundaries,
policy, retries, approval, budgets and state changes. Use the model for bounded
interpretation, synthesis, classification or selection among explicitly allowed
options. Define what happens when the model is unavailable or uncertain.

For long-running actions, document checkpoints, leases/locks, retries,
compensation, expiration, cancellation and resume semantics. Do not claim that
an MCP server or model prompt supplies durable execution or policy enforcement.

## Evaluation scenarios

Run nominal, missing data, unauthorized calls, malformed tool results,
malicious retrieved instructions, timeout/retry, concurrent writes, duplicate
requests, hallucinated IDs, prompt injection and interrupted execution.
Measure actual tool success and rule compliance separately from text quality.
