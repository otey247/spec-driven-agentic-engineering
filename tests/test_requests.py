from __future__ import annotations

import pytest


@pytest.mark.requirement("REQ-002")
def test_create_request_sets_pending_and_location(client, auth):
    response = client.post("/api/requests", headers=auth("alice"), json={"title": "  Upgrade the projector  ", "description": " Replace aging equipment "})
    assert response.status_code == 201
    item = response.json()
    assert item["title"] == "Upgrade the projector"
    assert item["status"] == "pending"
    assert item["created_by"] == "alice"
    assert item["version"] == 0
    assert response.headers["location"] == f"/api/requests/{item['id']}"
    assert client.get(response.headers["location"], headers=auth("alice")).json() == item


@pytest.mark.requirement("REQ-003")
@pytest.mark.parametrize("title,description", [("x", "A long enough description"), ("A valid title", "tiny"), ("   ", "valid description"), ("Hello", "   "), ("  ab  ", "valid description"), ("Valid title", "  abc  ")])
def test_bad_create_payload_is_rejected(client, auth, title, description):
    r = client.post("/api/requests", headers=auth("alice"), json={"title": title, "description": description})
    assert r.status_code == 422
    assert client.get("/api/requests", headers=auth("alice")).json() == []


@pytest.mark.requirement("REQ-005")
def test_requester_cannot_read_someone_elses_request(client, auth, create_request):
    other = create_request(user="eve")
    response = client.get(f"/api/requests/{other['id']}", headers=auth("alice"))
    assert response.status_code == 404
    assert client.get("/api/requests", headers=auth("alice")).json() == []
    assert len(client.get("/api/requests", headers=auth("bob")).json()) == 1


@pytest.mark.requirement("REQ-005")
def test_viewer_cannot_list_or_read(client, auth, create_request):
    record = create_request()
    assert client.get("/api/requests", headers=auth("viewer")).status_code == 403
    assert client.get(f"/api/requests/{record['id']}", headers=auth("viewer")).status_code == 404


@pytest.mark.requirement("REQ-010")
def test_filter_by_status(client, auth, create_request):
    r1 = create_request(title="Projector purchase")
    create_request(title="New meeting-room chairs")
    response = client.post(f"/api/requests/{r1['id']}/decision", headers=auth("bob"), json={"decision": "approve"})
    assert response.status_code == 200
    pending = client.get("/api/requests?status=pending", headers=auth("bob")).json()
    approved = client.get("/api/requests?status=approved", headers=auth("bob")).json()
    assert len(pending) == 1
    assert [r["id"] for r in approved] == [r1["id"]]
    assert client.get("/api/requests?status=unknown", headers=auth("bob")).status_code == 422


@pytest.mark.requirement("REQ-012")
def test_unknown_request_returns_404(client, auth):
    identifier = "00000000-0000-0000-0000-000000000000"
    assert client.get(f"/api/requests/{identifier}", headers=auth("alice")).status_code == 404
    assert client.post(f"/api/requests/{identifier}/decision", headers=auth("bob"), json={"decision": "approve"}).status_code == 404
