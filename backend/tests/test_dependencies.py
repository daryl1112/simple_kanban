"""Tests for card dependencies and, crucially, cycle prevention."""

from tests.conftest import make_card


def test_add_dependency(client, project):
    a = make_card(client, project["id"], title="A")
    b = make_card(client, project["id"], title="B")

    resp = client.post(f"/cards/{a['id']}/dependencies", json={"depends_on_id": b["id"]})
    assert resp.status_code == 201
    assert b["id"] in resp.json()["dependency_ids"]


def test_self_dependency_rejected(client, project):
    a = make_card(client, project["id"], title="A")
    resp = client.post(f"/cards/{a['id']}/dependencies", json={"depends_on_id": a["id"]})
    assert resp.status_code == 400


def test_direct_cycle_rejected(client, project):
    a = make_card(client, project["id"], title="A")
    b = make_card(client, project["id"], title="B")

    # A depends on B is fine...
    client.post(f"/cards/{a['id']}/dependencies", json={"depends_on_id": b["id"]})
    # ...but B depending on A closes a 2-node cycle and must be rejected.
    resp = client.post(f"/cards/{b['id']}/dependencies", json={"depends_on_id": a["id"]})
    assert resp.status_code == 400


def test_indirect_cycle_rejected(client, project):
    a = make_card(client, project["id"], title="A")
    b = make_card(client, project["id"], title="B")
    c = make_card(client, project["id"], title="C")

    # Build chain A -> B -> C, then C -> A would create a 3-node cycle.
    client.post(f"/cards/{a['id']}/dependencies", json={"depends_on_id": b["id"]})
    client.post(f"/cards/{b['id']}/dependencies", json={"depends_on_id": c["id"]})
    resp = client.post(f"/cards/{c['id']}/dependencies", json={"depends_on_id": a["id"]})
    assert resp.status_code == 400


def test_cross_project_dependency_rejected(client, project):
    other = client.post("/projects", json={"name": "Other"}).json()
    a = make_card(client, project["id"], title="A")
    b = make_card(client, other["id"], title="B")

    resp = client.post(f"/cards/{a['id']}/dependencies", json={"depends_on_id": b["id"]})
    assert resp.status_code == 400


def test_remove_dependency(client, project):
    a = make_card(client, project["id"], title="A")
    b = make_card(client, project["id"], title="B")
    client.post(f"/cards/{a['id']}/dependencies", json={"depends_on_id": b["id"]})

    resp = client.delete(f"/cards/{a['id']}/dependencies/{b['id']}")
    assert resp.status_code == 200
    assert resp.json()["dependency_ids"] == []


def test_list_dependencies(client, project):
    a = make_card(client, project["id"], title="A")
    b = make_card(client, project["id"], title="B")
    client.post(f"/cards/{a['id']}/dependencies", json={"depends_on_id": b["id"]})

    resp = client.get(f"/cards/{a['id']}/dependencies")
    assert resp.status_code == 200
    assert [c["id"] for c in resp.json()] == [b["id"]]


def test_duplicate_dependency_is_idempotent(client, project):
    a = make_card(client, project["id"], title="A")
    b = make_card(client, project["id"], title="B")
    client.post(f"/cards/{a['id']}/dependencies", json={"depends_on_id": b["id"]})
    resp = client.post(f"/cards/{a['id']}/dependencies", json={"depends_on_id": b["id"]})
    assert resp.status_code == 201
    assert resp.json()["dependency_ids"].count(b["id"]) == 1
