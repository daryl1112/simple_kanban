"""Tests for card comments (Markdown bodies)."""

from tests.conftest import make_card


def test_add_and_list_comments(client, project):
    card = make_card(client, project["id"])
    resp = client.post(f"/cards/{card['id']}/comments", json={"body": "**looks good**"})
    assert resp.status_code == 201
    assert resp.json()["body"] == "**looks good**"  # Markdown stored verbatim

    listing = client.get(f"/cards/{card['id']}/comments")
    assert listing.status_code == 200
    assert len(listing.json()) == 1


def test_comment_with_author(client, project, user):
    card = make_card(client, project["id"])
    resp = client.post(
        f"/cards/{card['id']}/comments",
        json={"body": "mine", "author_id": user["id"]},
    )
    assert resp.status_code == 201
    assert resp.json()["author_id"] == user["id"]


def test_comment_with_bad_author_rejected(client, project):
    card = make_card(client, project["id"])
    resp = client.post(
        f"/cards/{card['id']}/comments", json={"body": "x", "author_id": 999}
    )
    assert resp.status_code == 400


def test_empty_comment_rejected(client, project):
    card = make_card(client, project["id"])
    assert client.post(f"/cards/{card['id']}/comments", json={"body": ""}).status_code == 422


def test_delete_comment(client, project):
    card = make_card(client, project["id"])
    comment = client.post(f"/cards/{card['id']}/comments", json={"body": "temp"}).json()
    assert client.delete(f"/comments/{comment['id']}").status_code == 204
    assert client.get(f"/cards/{card['id']}/comments").json() == []


def test_comment_on_missing_card_returns_404(client):
    assert client.post("/cards/999/comments", json={"body": "x"}).status_code == 404
