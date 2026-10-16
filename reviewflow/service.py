"""Transactional request and approval operations.

All access control decisions are enforced here, never trusted to the UI or an agent.
"""
from __future__ import annotations

import sqlite3
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from importlib.resources import files
from pathlib import Path
from typing import Iterator

from .auth import Actor


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class DomainError(Exception):
    def __init__(self, status_code: int, detail: str):
        super().__init__(detail)
        self.status_code = status_code
        self.detail = detail


class ReviewService:
    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)
        if self.db_path == ":memory:":
            raise ValueError("Use a file-backed SQLite database for concurrent requests")
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as conn:
            conn.executescript(files("reviewflow").joinpath("schema.sql").read_text(encoding="utf-8"))

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        conn = sqlite3.connect(self.db_path, timeout=10, isolation_level=None)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys=ON")
        conn.execute("PRAGMA busy_timeout=10000")
        try:
            yield conn
        finally:
            conn.close()

    @staticmethod
    def require_role(actor: Actor, role: str) -> None:
        if role not in actor.roles:
            raise DomainError(403, "Not authorized for this action")

    @staticmethod
    def can_read(actor: Actor, item: dict) -> bool:
        return item["created_by"] == actor.user_id or "approver" in actor.roles

    def create(self, actor: Actor, title: str, description: str) -> dict:
        self.require_role(actor, "requester")
        identifier = str(uuid.uuid4())
        time = now_iso()
        with self.connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                conn.execute(
                    "INSERT INTO requests(id,title,description,created_by,status,created_at,updated_at,version) "
                    "VALUES(?,?,?,?,'pending',?,?,0)",
                    (identifier, title, description, actor.user_id, time, time),
                )
                conn.execute(
                    "INSERT INTO audit_events(request_id,actor_id,action,note,at) VALUES(?,?,'created','',?)",
                    (identifier, actor.user_id, time),
                )
                conn.execute("COMMIT")
            except Exception:
                conn.execute("ROLLBACK")
                raise
        return self.get(actor, identifier)

    def get(self, actor: Actor, identifier: str) -> dict:
        with self.connect() as conn:
            row = conn.execute("SELECT * FROM requests WHERE id=?", (identifier,)).fetchone()
        if row is None:
            raise DomainError(404, "Request not found")
        item = dict(row)
        if not self.can_read(actor, item):
            # Hide existence from other requesters and viewers.
            raise DomainError(404, "Request not found")
        return item

    def list(self, actor: Actor, status: str | None = None) -> list[dict]:
        if "approver" not in actor.roles and "requester" not in actor.roles:
            raise DomainError(403, "Not authorized to list requests")
        filters = []
        values: list[str] = []
        if "approver" not in actor.roles:
            filters.append("created_by=?")
            values.append(actor.user_id)
        if status is not None:
            filters.append("status=?")
            values.append(status)
        query = "SELECT * FROM requests"
        if filters:
            query += " WHERE " + " AND ".join(filters)
        query += " ORDER BY created_at DESC, id DESC LIMIT 100"
        with self.connect() as conn:
            return [dict(row) for row in conn.execute(query, values).fetchall()]

    def decide(self, actor: Actor, identifier: str, decision: str, note: str) -> dict:
        self.require_role(actor, "approver")
        if decision == "reject" and not note.strip():
            raise DomainError(422, "A rejection reason is required")
        status = {"approve": "approved", "reject": "rejected"}.get(decision)
        if status is None:
            raise DomainError(422, "Invalid decision")
        with self.connect() as conn:
            conn.execute("BEGIN IMMEDIATE")
            try:
                row = conn.execute("SELECT * FROM requests WHERE id=?", (identifier,)).fetchone()
                if row is None:
                    raise DomainError(404, "Request not found")
                record = dict(row)
                if actor.user_id == record["created_by"]:  # MAKER_CHECKER_GUARD
                    raise DomainError(403, "Creators cannot decide their own requests")
                if record["status"] != "pending":
                    raise DomainError(409, "Only pending requests may be decided")
                time = now_iso()
                conn.execute(
                    "UPDATE requests SET status=?,updated_at=?,version=version+1 WHERE id=?",
                    (status, time, identifier),
                )
                conn.execute(
                    "INSERT INTO audit_events(request_id,actor_id,action,note,at) VALUES(?,?,?,?,?)",
                    (identifier, actor.user_id, status, note, time),
                )
                conn.execute("COMMIT")
            except Exception:
                conn.execute("ROLLBACK")
                raise
        return self.get(actor, identifier)

    def audit(self, actor: Actor, identifier: str) -> list[dict]:
        self.get(actor, identifier)
        with self.connect() as conn:
            return [dict(row) for row in conn.execute(
                "SELECT id,request_id,actor_id,action,note,at FROM audit_events WHERE request_id=? ORDER BY id",
                (identifier,),
            )]

    def health(self) -> bool:
        with self.connect() as conn:
            return conn.execute("SELECT 1").fetchone()[0] == 1
