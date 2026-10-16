from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from reviewflow.api import create_app
from reviewflow.auth import resolve_demo_actor


@pytest.mark.requirement("REQ-013")
def test_local_demo_page_displays_request_actions(client):
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]
    assert 'id="newRequest"' in response.text
    assert 'id="requests"' in response.text
    assert "Requests for review" in response.text


@pytest.mark.requirement("REQ-013")
def test_non_demo_app_does_not_serve_local_demo_page(tmp_path):
    app = create_app(tmp_path / "test.db", identity_resolver=resolve_demo_actor)
    with TestClient(app) as client:
        assert client.get("/").status_code == 404
