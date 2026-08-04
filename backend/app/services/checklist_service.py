"""Business logic for checklists and their items.

Kept separate from card_service so each module owns a single concern. Card
existence checks reuse `card_service._get_card_or_raise`.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.logging import get_logger
from app.models import Checklist, ChecklistItem
from app.schemas import (
    ChecklistCreate,
    ChecklistItemCreate,
    ChecklistItemUpdate,
    ChecklistUpdate,
)
from app.services.card_service import _get_card_or_raise
from app.services.errors import NotFoundError

logger = get_logger(__name__)


def _get_checklist_or_raise(db: Session, checklist_id: int) -> Checklist:
    """Fetch a checklist with items eagerly loaded, or raise NotFoundError."""
    stmt = (
        select(Checklist)
        .where(Checklist.id == checklist_id)
        .options(selectinload(Checklist.items))
    )
    checklist = db.scalars(stmt).unique().one_or_none()
    if checklist is None:
        raise NotFoundError(f"Checklist {checklist_id} not found")
    return checklist


def _get_item_or_raise(db: Session, item_id: int) -> ChecklistItem:
    """Fetch a checklist item or raise NotFoundError."""
    item = db.get(ChecklistItem, item_id)
    if item is None:
        raise NotFoundError(f"Checklist item {item_id} not found")
    return item


def create_checklist(db: Session, card_id: int, payload: ChecklistCreate) -> Checklist:
    """Create a checklist on a card."""
    _get_card_or_raise(db, card_id)  # ensure the card exists
    checklist = Checklist(card_id=card_id, title=payload.title)
    db.add(checklist)
    db.commit()
    logger.info("Created checklist id=%s on card=%s", checklist.id, card_id)
    return _get_checklist_or_raise(db, checklist.id)


def list_checklists(db: Session, card_id: int) -> list[Checklist]:
    """Return a card's checklists, ordered by id."""
    _get_card_or_raise(db, card_id)
    stmt = (
        select(Checklist)
        .where(Checklist.card_id == card_id)
        .order_by(Checklist.id)
        .options(selectinload(Checklist.items))
    )
    return list(db.scalars(stmt).unique())


def update_checklist(db: Session, checklist_id: int, payload: ChecklistUpdate) -> Checklist:
    """Rename a checklist."""
    checklist = _get_checklist_or_raise(db, checklist_id)
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(checklist, field, value)
    db.commit()
    logger.info("Updated checklist id=%s fields=%s", checklist_id, list(data))
    return _get_checklist_or_raise(db, checklist_id)


def delete_checklist(db: Session, checklist_id: int) -> None:
    """Delete a checklist and its items (via cascade)."""
    checklist = _get_checklist_or_raise(db, checklist_id)
    db.delete(checklist)
    db.commit()
    logger.info("Deleted checklist id=%s", checklist_id)


def add_item(db: Session, checklist_id: int, payload: ChecklistItemCreate) -> ChecklistItem:
    """Add an item to a checklist."""
    _get_checklist_or_raise(db, checklist_id)
    item = ChecklistItem(
        checklist_id=checklist_id,
        text=payload.text,
        is_completed=payload.is_completed,
    )
    db.add(item)
    db.commit()
    db.refresh(item)
    logger.info("Added item id=%s to checklist=%s", item.id, checklist_id)
    return item


def update_item(db: Session, item_id: int, payload: ChecklistItemUpdate) -> ChecklistItem:
    """Edit an item's text and/or toggle its completion state."""
    item = _get_item_or_raise(db, item_id)
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(item, field, value)
    db.commit()
    db.refresh(item)
    logger.info("Updated checklist item id=%s fields=%s", item_id, list(data))
    return item


def delete_item(db: Session, item_id: int) -> None:
    """Delete a single checklist item."""
    item = _get_item_or_raise(db, item_id)
    db.delete(item)
    db.commit()
    logger.info("Deleted checklist item id=%s", item_id)
