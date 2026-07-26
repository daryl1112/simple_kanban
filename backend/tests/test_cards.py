"""Tests for card CRUD, status moves, assignment, and the board view."""

from tests.conftest import make_card


def test_create_card_defaults_to_backlog(client, project):
    card = make_card(client, project["id"], title="First")
    assert card["status"] == "backlog"
    assert card["assignee_id"] is None
    assert card["dependency_ids"] == []


def test_create_card_with_markdown_description(client, project):
    card = make_card(client, project["id"], description="## Heading\n- item")
    assert card["description"] == "## Heading\n- item"


def test_move_card_between_statuses(client, project):
    card = make_card(client, project["id"])
    resp = client.patch(f"/cards/{card['id']}", json={"status": "in_progress"})
    assert resp.status_code == 200
    assert resp.json()["status"] == "in_progress"


def test_assign_and_unassign_card(client, project, user):
    card = make_card(client, project["id"])
    assigned = client.patch(f"/cards/{card['id']}", json={"assignee_id": user["id"]})
    assert assigned.json()["assignee_id"] == user["id"]

    unassigned = client.patch(f"/cards/{card['id']}", json={"assignee_id": None})
    assert unassigned.json()["assignee_id"] is None


def test_assign_nonexistent_user_rejected(client, project):
    card = make_card(client, project["id"])
    resp = client.patch(f"/cards/{card['id']}", json={"assignee_id": 4242})
    assert resp.status_code == 400


def test_delete_card(client, project):
    card = make_card(client, project["id"])
    assert client.delete(f"/cards/{card['id']}").status_code == 204
    assert client.get(f"/cards/{card['id']}").status_code == 404


def test_board_groups_cards_by_status(client, project):
    make_card(client, project["id"], title="a", status="backlog")
    make_card(client, project["id"], title="b", status="review")

    resp = client.get(f"/projects/{project['id']}/board")
    assert resp.status_code == 200
    board = resp.json()

    # Five columns, in the documented order.
    statuses = [col["status"] for col in board["columns"]]
    assert statuses == ["backlog", "approved", "in_progress", "review", "completed"]

    counts = {col["status"]: len(col["cards"]) for col in board["columns"]}
    assert counts["backlog"] == 1
    assert counts["review"] == 1
    assert counts["approved"] == 0
