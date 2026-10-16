from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor

import pytest


@pytest.mark.requirement("REQ-014")
def test_requester_cannot_approve_own_request(client, auth, create_request):
    """Regression gate: a dual-role actor still cannot approve their own item."""
    record = create_request(user="eve")
    response = client.post(f"/api/requests/{record['id']}/decision", headers=auth("eve"), json={"decision": "approve"})
    assert response.status_code == 403
    assert client.get(f"/api/requests/{record['id']}", headers=auth("eve")).json()["status"] == "pending"


@pytest.mark.requirement("REQ-014")
def test_requester_cannot_reject_own_request(client, auth, create_request):
    record = create_request(user="eve")
    response = client.post(f"/api/requests/{record['id']}/decision", headers=auth("eve"), json={"decision": "reject", "note": "Too costly"})
    assert response.status_code == 403


@pytest.mark.requirement("REQ-006")
def test_approver_can_approve_another_persons_request(client, auth, create_request):
    record = create_request()
    response = client.post(f"/api/requests/{record['id']}/decision", headers=auth("bob"), json={"decision": "approve", "note": "Budget confirmed"})
    assert response.status_code == 200
    assert response.json()["status"] == "approved"
    assert response.json()["version"] == 1


@pytest.mark.requirement("REQ-006")
def test_approver_can_reject_with_reason(client, auth, create_request):
    record = create_request()
    response = client.post(f"/api/requests/{record['id']}/decision", headers=auth("charlie"), json={"decision": "reject", "note": "Not approved for Q4"})
    assert response.status_code == 200
    assert response.json()["status"] == "rejected"


@pytest.mark.requirement("REQ-007")
def test_rejection_requires_reason(client, auth, create_request):
    record = create_request()
    response = client.post(f"/api/requests/{record['id']}/decision", headers=auth("bob"), json={"decision": "reject", "note": "   "})
    assert response.status_code == 422
    assert client.get(f"/api/requests/{record['id']}", headers=auth("alice")).json()["status"] == "pending"


@pytest.mark.requirement("REQ-008")
def test_second_decision_is_conflict(client, auth, create_request):
    record = create_request()
    path = f"/api/requests/{record['id']}/decision"
    assert client.post(path, headers=auth("bob"), json={"decision": "approve"}).status_code == 200
    assert client.post(path, headers=auth("charlie"), json={"decision": "reject", "note": "Disagree"}).status_code == 409
    assert client.get(f"/api/requests/{record['id']}", headers=auth("bob")).json()["status"] == "approved"


@pytest.mark.requirement("REQ-009")
def test_concurrent_decisions_commit_once(client, auth, create_request):
    record = create_request()
    path = f"/api/requests/{record['id']}/decision"

    def approve(who):
        return client.post(path, headers=auth(who), json={"decision": "approve"}).status_code

    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(approve, ["bob", "charlie"]))
    assert sorted(results) == [200, 409]
    audit = client.get(f"/api/requests/{record['id']}/audit", headers=auth("alice")).json()
    assert [event["action"] for event in audit] == ["created", "approved"]


@pytest.mark.requirement("REQ-008")
def test_invalid_decision_is_rejected(client, auth, create_request):
    record = create_request()
    response = client.post(f"/api/requests/{record['id']}/decision", headers=auth("bob"), json={"decision": "escalate"})
    assert response.status_code == 422
