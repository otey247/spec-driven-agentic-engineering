# Feature specification: ReviewFlow approval workflow

**Status:** Accepted for reference implementation  
**Owner:** Example engineering team  
**Scope:** Local training workflow; not a deployable enterprise identity solution  
**Related design:** `docs/architecture.md`  
**Traceability:** `specs/traceability.json`

## Problem and users

A requester needs to submit a business request and see its progress. A separate
approver must accept or reject it. All allowed state changes need traceable
records. The example must make it impossible for a person with both requester
and approver roles to approve their own request.

Actors: requester; approver; viewer without privileges; dual-role user.

## Scope

Included: REST API, local demo page, immutable audit event insertion, SQLite,
server-side access control, transactional single decision, automated tests.

Excluded: enterprise SSO, production authorization provisioning, notifications,
uploads, monetary approval limits, database migration lifecycle, rate limiting,
operational monitoring, distribution, accessibility conformance audit.

## Requirements and acceptance criteria

### REQ-001: Authenticated access

API data routes require valid Bearer identity. Missing or incorrect credentials
return HTTP 401. Identity is derived from the resolver rather than a client
supplied user ID.

### REQ-002: Create a request

A requester can create a title and description. The server assigns a UUID,
creator identity, UTC timestamps, status `pending` and version 0. Return HTTP 201
and a Location header. Immediately persist an associated `created` audit event.

### REQ-003: Validate user inputs

Titles must be 3-120 characters; descriptions 5-4000 characters. Leading and
trailing spaces are trimmed. Missing, blank or out-of-range inputs are rejected
with HTTP 422 and no stored request.

### REQ-004: Server-side role authorization

Only requesters may create. Only approvers may decide. Role checks run in the
service, independent from UI state. Unauthorized attempts return HTTP 403.

### REQ-005: Request and audit visibility

Requesters may read their own requests and audits. Approvers may read all
requests and audits. Viewers cannot list requests. Unknown or otherwise hidden
requests return HTTP 404. Requester list results exclude others' records.

### REQ-006: Allowed approval actions

An approver other than the request creator may approve or reject a pending
request. Approval sets `approved`; rejection sets `rejected`. Version increments
once and the server returns updated state.

### REQ-007: Rejection reason

A rejection requires a nonblank note of at most 500 characters. Otherwise the
API returns HTTP 422 without mutating the request.

### REQ-008: Only one final decision

A request may move from pending to exactly one terminal decision. Attempts to
change an approved or rejected request return HTTP 409. Invalid decisions
return HTTP 422.

### REQ-009: Atomic decision under concurrency

Two simultaneous approvers must not both succeed. Exactly one decision
commits (HTTP 200); the other observes HTTP 409. Only one terminal audit event
is written. The implementation uses a transaction to serialize writers.

### REQ-010: Filter requests by status

List endpoint accepts pending, approved and rejected status filters. Invalid
filters return HTTP 422.

### REQ-011: Fail closed without identity integration

Application factory refuses startup without an identity resolver or explicit
local-only demo mode. Demo mode and production resolver cannot be active at
once. The CLI binds only loopback when demo mode is enabled.

### REQ-012: Health and missing records

Unknown request IDs return HTTP 404. GET /health checks storage connectivity
and returns 200 with `status: ok` when usable.

### REQ-013: Local demo page is isolated

Only explicit demo mode exposes the local browser page for creating and
reviewing requests. It has a request form and a visible request list. With an
externally supplied identity resolver and no demo flag, `/` returns HTTP 404.
The page must not be treated as the security boundary; API checks are required.

### REQ-014: Maker-checker separation

**Given** an actor with both requester and approver roles created a pending
request, **when** that actor attempts to approve or reject it, **then** the API
returns HTTP 403. Status remains pending and no successful decision audit event
is created. Role membership must never override this condition.

### REQ-016: Accepted action auditability

Creation and successful decisions write UTC time, actor identity, action and
optional note in the same database transaction as the state change. Rejected
attempts must not be recorded as accepted actions. Access to the audit history
follows the same visibility rule as access to the associated request.

## Nonfunctional requirements

- NFR-01: Store all records and audit events in a file-backed local SQLite DB.
- NFR-02: Use parameterized SQL queries for all user-controlled values.
- NFR-03: A failed operation must not leave a partial committed state change.
- NFR-04: Limit list results to 100 rows for the reference exercise.
- NFR-05: Never start the demo server on a non-loopback interface.
- NFR-06: Require deterministic tests for security-sensitive behavior.

## State transitions

```text
pending --approve--> approved
pending --reject---> rejected
approved/rejected --any decision--> HTTP 409 (no change)
creator self-decision ---------> HTTP 403 (no change)
```

## Verification contract

Run `python scripts/verify.py` for the accepted implementation. Run
`python scripts/acceptance_demo.py` to demonstrate a deliberately injected
maker-checker defect failing the same verification command.

The executable requirement-test matrix lives in `specs/traceability.json`.
The guard demonstration is a training tool, not a substitute for a security audit.

## Open questions and deployment boundaries

Before any production use: select an identity provider, implement token signature,
issuer, audience and expiry validation, add migrations, rate limits, observability,
secrets management, HTTPS, operational backups and incident handling; perform
threat modeling and deployment-specific performance and accessibility testing.
