from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from reviewflow.api import create_app

TOKENS = {
    "alice": "alice-local-demo",
    "bob": "bob-local-demo",
    "charlie": "charlie-local-demo",
    "eve": "eve-local-demo",
    "viewer": "viewer-local-demo",
}


@pytest.fixture
def client(tmp_path):
    app = create_app(tmp_path / "test.db", demo_mode=True)
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def auth():
    def header(user: str) -> dict[str, str]:
        return {"Authorization": f"Bearer {TOKENS[user]}"}
    return header


@pytest.fixture
def create_request(client, auth):
    def create(user="alice", title="Upgrade office projector", description="Replace failed display hardware"):
        response = client.post("/api/requests", headers=auth(user), json={"title": title, "description": description})
        assert response.status_code == 201, response.text
        return response.json()
    return create
