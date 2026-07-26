"""Tests for the user endpoints."""


def test_create_and_get_user(client):
    resp = client.post("/users", json={"name": "Grace", "email": "grace@example.com"})
    assert resp.status_code == 201
    body = resp.json()
    assert body["name"] == "Grace"

    fetched = client.get(f"/users/{body['id']}")
    assert fetched.status_code == 200


def test_duplicate_email_rejected(client):
    client.post("/users", json={"name": "A", "email": "dup@example.com"})
    # A second user with the same email violates the unique constraint.
    resp = client.post("/users", json={"name": "B", "email": "dup@example.com"})
    assert resp.status_code == 400


def test_invalid_email_rejected(client):
    resp = client.post("/users", json={"name": "A", "email": "not-an-email"})
    assert resp.status_code == 422


def test_update_and_delete_user(client, user):
    resp = client.patch(f"/users/{user['id']}", json={"name": "Ada L."})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Ada L."

    assert client.delete(f"/users/{user['id']}").status_code == 204
    assert client.get(f"/users/{user['id']}").status_code == 404
