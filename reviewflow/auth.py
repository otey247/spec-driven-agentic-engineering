"""Fail-closed identity integration; intentionally local demo tokens only.

Production applications must replace the demo resolver with an identity-provider-backed
resolver that verifies signatures, audience, issuer, expiry and authorizations.
"""
from __future__ import annotations

from dataclasses import dataclass
from hmac import compare_digest
from typing import FrozenSet

from fastapi import HTTPException


@dataclass(frozen=True, slots=True)
class Actor:
    user_id: str
    roles: FrozenSet[str]


DEMO_IDENTITIES: dict[str, Actor] = {
    "alice-local-demo": Actor("alice", frozenset({"requester"})),
    "bob-local-demo": Actor("bob", frozenset({"approver"})),
    "charlie-local-demo": Actor("charlie", frozenset({"approver"})),
    "eve-local-demo": Actor("eve", frozenset({"requester", "approver"})),
    "viewer-local-demo": Actor("viewer", frozenset({"viewer"})),
}


def resolve_demo_actor(authorization: str | None) -> Actor:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Bearer authentication required")
    token = authorization[len("Bearer "):]
    if not token or token.strip() != token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    for known, actor in DEMO_IDENTITIES.items():
        if compare_digest(token, known):
            return actor
    raise HTTPException(status_code=401, detail="Invalid credentials")
