"""Tests for the project endpoints."""


def test_create_and_get_project(client):
    resp = client.post("/projects", json={"name": "Apollo", "description": "**bold**"})
    assert resp.status_code == 201
    created = resp.json()
    assert created["name"] == "Apollo"
    assert created["description"] == "**bold**"  # Markdown stored verbatim

    fetched = client.get(f"/projects/{created['id']}")
    assert fetched.status_code == 200
    assert fetched.json()["id"] == created["id"]


def test_list_projects(client):
    client.post("/projects", json={"name": "A"})
    client.post("/projects", json={"name": "B"})
    resp = client.get("/projects")
    assert resp.status_code == 200
    assert len(resp.json()) == 2


def test_update_project(client, project):
    resp = client.patch(f"/projects/{project['id']}", json={"name": "Renamed"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Renamed"


def test_delete_project(client, project):
    resp = client.delete(f"/projects/{project['id']}")
    assert resp.status_code == 204
    assert client.get(f"/projects/{project['id']}").status_code == 404


def test_get_missing_project_returns_404(client):
    assert client.get("/projects/999").status_code == 404


def test_create_project_requires_name(client):
    assert client.post("/projects", json={"name": ""}).status_code == 422
