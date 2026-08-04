"""Tests for checklists and checklist items, including badge aggregation."""

from tests.conftest import make_card


def _make_checklist(client, card_id, title="Acceptance criteria"):
    resp = client.post(f"/cards/{card_id}/checklists", json={"title": title})
    assert resp.status_code == 201, resp.text
    return resp.json()


def test_create_checklist_starts_empty(client, project):
    card = make_card(client, project["id"])
    checklist = _make_checklist(client, card["id"])
    assert checklist["title"] == "Acceptance criteria"
    assert checklist["items"] == []
    assert checklist["total_count"] == 0
    assert checklist["completed_count"] == 0


def test_add_items_and_progress_counts(client, project):
    card = make_card(client, project["id"])
    checklist = _make_checklist(client, card["id"])

    client.post(f"/checklists/{checklist['id']}/items", json={"text": "First"})
    second = client.post(
        f"/checklists/{checklist['id']}/items", json={"text": "Second"}
    ).json()
    assert second["is_completed"] is False

    listing = client.get(f"/cards/{card['id']}/checklists").json()
    assert listing[0]["total_count"] == 2
    assert listing[0]["completed_count"] == 0


def test_toggle_item_updates_completed_count(client, project):
    card = make_card(client, project["id"])
    checklist = _make_checklist(client, card["id"])
    item = client.post(
        f"/checklists/{checklist['id']}/items", json={"text": "Do the thing"}
    ).json()

    toggled = client.patch(
        f"/checklist-items/{item['id']}", json={"is_completed": True}
    )
    assert toggled.status_code == 200
    assert toggled.json()["is_completed"] is True

    checklist_after = client.get(f"/cards/{card['id']}/checklists").json()[0]
    assert checklist_after["completed_count"] == 1
    assert checklist_after["total_count"] == 1


def test_edit_item_text(client, project):
    card = make_card(client, project["id"])
    checklist = _make_checklist(client, card["id"])
    item = client.post(
        f"/checklists/{checklist['id']}/items", json={"text": "old"}
    ).json()

    resp = client.patch(f"/checklist-items/{item['id']}", json={"text": "new"})
    assert resp.status_code == 200
    assert resp.json()["text"] == "new"


def test_rename_checklist(client, project):
    card = make_card(client, project["id"])
    checklist = _make_checklist(client, card["id"])
    resp = client.patch(f"/checklists/{checklist['id']}", json={"title": "QA"})
    assert resp.status_code == 200
    assert resp.json()["title"] == "QA"


def test_delete_item(client, project):
    card = make_card(client, project["id"])
    checklist = _make_checklist(client, card["id"])
    item = client.post(
        f"/checklists/{checklist['id']}/items", json={"text": "temp"}
    ).json()

    assert client.delete(f"/checklist-items/{item['id']}").status_code == 204
    assert client.get(f"/cards/{card['id']}/checklists").json()[0]["total_count"] == 0


def test_delete_checklist_removes_its_items(client, project):
    card = make_card(client, project["id"])
    checklist = _make_checklist(client, card["id"])
    client.post(f"/checklists/{checklist['id']}/items", json={"text": "a"})

    assert client.delete(f"/checklists/{checklist['id']}").status_code == 204
    assert client.get(f"/cards/{card['id']}/checklists").json() == []


def test_card_and_board_expose_badge_counts(client, project):
    """The card (and thus the board) reports aggregate item counts for the badge."""
    card = make_card(client, project["id"])
    cl1 = _make_checklist(client, card["id"], "List one")
    cl2 = _make_checklist(client, card["id"], "List two")

    # 3 items total, 1 completed, spread across two checklists.
    i1 = client.post(f"/checklists/{cl1['id']}/items", json={"text": "a"}).json()
    client.post(f"/checklists/{cl1['id']}/items", json={"text": "b"})
    client.post(f"/checklists/{cl2['id']}/items", json={"text": "c"})
    client.patch(f"/checklist-items/{i1['id']}", json={"is_completed": True})

    fetched = client.get(f"/cards/{card['id']}").json()
    assert fetched["checklist_items_total"] == 3
    assert fetched["checklist_items_completed"] == 1
    assert len(fetched["checklists"]) == 2

    # Same numbers must surface through the board view.
    board = client.get(f"/projects/{project['id']}/board").json()
    board_card = board["columns"][0]["cards"][0]
    assert board_card["checklist_items_total"] == 3
    assert board_card["checklist_items_completed"] == 1


def test_checklist_on_missing_card_returns_404(client):
    assert client.post("/cards/999/checklists", json={"title": "x"}).status_code == 404


def test_item_on_missing_checklist_returns_404(client):
    assert client.post("/checklists/999/items", json={"text": "x"}).status_code == 404


def test_deleting_card_cascades_to_checklists(client, project):
    card = make_card(client, project["id"])
    checklist = _make_checklist(client, card["id"])
    client.post(f"/checklists/{checklist['id']}/items", json={"text": "a"})

    assert client.delete(f"/cards/{card['id']}").status_code == 204
    # The checklist is gone with its card.
    assert client.patch(f"/checklists/{checklist['id']}", json={"title": "z"}).status_code == 404
