from __future__ import annotations

import pytest


@pytest.mark.requirement("REQ-016")
def test_audit_has_actor_action_note_and_time(client, auth, create_request):
    record = create_request()
    path = f"/api/requests/{record['id']}"
    response = client.post(f"{path}/decision", headers=auth("bob"), json={"decision": "approve", "note": "Funds available"})
    assert response.status_code == 200
    events = client.get(f"{path}/audit", headers=auth("alice")).json()
    assert len(events) == 2
    assert [e["action"] for e in events] == ["created", "approved"]
    assert [e["actor_id"] for e in events] == ["alice", "bob"]
    assert events[1]["note"] == "Funds available"
    assert all(e["at"].endswith("+00:00") for e in events)


@pytest.mark.requirement("REQ-016")
def test_failed_decisions_do_not_append_success_audit(client, auth, create_request):
    record = create_request(user="eve")
    path = f"/api/requests/{record['id']}"
    response = client.post(f"{path}/decision", headers=auth("eve"), json={"decision": "approve"})
    assert response.status_code == 403
    events = client.get(f"{path}/audit", headers=auth("eve")).json()
    assert [e["action"] for e in events] == ["created"]


@pytest.mark.requirement("REQ-005")
def test_audit_is_not_visible_to_other_requesters(client, auth, create_request):
    record = create_request(user="eve")
    response = client.get(f"/api/requests/{record['id']}/audit", headers=auth("alice"))
    assert response.status_code == 404


@pytest.mark.requirement("REQ-012")
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
