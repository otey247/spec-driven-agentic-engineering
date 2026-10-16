from __future__ import annotations

import pytest

from reviewflow.api import create_app


@pytest.mark.requirement("REQ-001")
def test_missing_authentication_is_rejected(client):
    assert client.get("/api/requests").status_code == 401
    assert client.post("/api/requests", json={"title": "Hello", "description": "A valid description"}).status_code == 401


@pytest.mark.requirement("REQ-001")
def test_invalid_token_is_rejected(client):
    response = client.get("/api/requests", headers={"Authorization": "Bearer not-a-valid-token"})
    assert response.status_code == 401


@pytest.mark.requirement("REQ-004")
def test_non_requester_cannot_create(client, auth):
    response = client.post("/api/requests", headers=auth("bob"), json={"title": "Legal title", "description": "Valid description"})
    assert response.status_code == 403


@pytest.mark.requirement("REQ-004")
def test_non_approver_cannot_decide(client, auth, create_request):
    record = create_request()
    response = client.post(f"/api/requests/{record['id']}/decision", headers=auth("alice"), json={"decision": "approve"})
    assert response.status_code == 403


@pytest.mark.requirement("REQ-011")
def test_service_fails_closed_without_identity_provider(tmp_path):
    with pytest.raises(RuntimeError, match="identity provider"):
        create_app(tmp_path / "blocked.db")


@pytest.mark.requirement("REQ-011")
def test_demo_does_not_allow_second_auth_provider(tmp_path):
    with pytest.raises(ValueError, match="either"):
        create_app(tmp_path / "blocked.db", demo_mode=True, identity_resolver=lambda x: x)
