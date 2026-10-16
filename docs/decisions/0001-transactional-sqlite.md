# ADR-0001: Use file-backed SQLite for the training reference

Status: Accepted  
Date: 2026-10-16

## Context

The reference must demonstrate an actual atomic approval transition with an
audit record and a reproducible concurrency test. It should run on a developer
computer without Docker or a cloud account.

## Decision

Use file-backed SQLite and serialized write transactions (`BEGIN IMMEDIATE`).
Open a connection per domain operation and keep authorization inside the
transaction for decisions.

## Consequences

- Runs with one Python process and a single file; training does not depend on cloud services.
- Enables tests proving only one concurrent approval commits.
- Does not demonstrate horizontal-scale distributed locking or migrations.
- A production deployment would evaluate PostgreSQL with explicit migration,
  operational, monitoring and retention strategies.
