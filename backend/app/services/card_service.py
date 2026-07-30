"""Business logic for cards, including board assembly and assignment.

Dependency wiring lives in `dependency_service` to keep each module focused on
a single responsibility; this module handles card CRUD, status moves, and the
board view.
"""

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.core.logging import get_logger
from app.models import Card, CardStatus, User
from app.schemas import CardCreate, CardUpdate
from app.schemas.card import BoardColumn, BoardRead, CardRead
from app.services.errors import NotFoundError, ValidationError
from app.services.project_service import get_project

logger = get_logger(__name__)


def _load_options():
    """Eager-load relationships needed to serialise a card in one query set."""
    return (selectinload(Card.dependencies), selectinload(Card.comments))


def to_read_model(card: Card) -> CardRead:
    """Convert an ORM card into its API representation.

    Flattens the dependency relationship into a list of ids so the response is
    stable and free of circular references.
    """
    data = CardRead.model_validate(card)
    data.dependency_ids = sorted(dep.id for dep in card.dependencies)
    return data


def _get_card_or_raise(db: Session, card_id: int) -> Card:
    """Fetch a card with relationships eagerly loaded, or raise NotFoundError."""
    stmt = select(Card).where(Card.id == card_id).options(*_load_options())
    card = db.scalars(stmt).unique().one_or_none()
    if card is None:
        raise NotFoundError(f"Card {card_id} not found")
    return card


def _validate_assignee(db: Session, assignee_id: int | None) -> None:
    """Ensure an assignee, if provided, refers to a real user."""
    if assignee_id is not None and db.get(User, assignee_id) is None:
        raise ValidationError(f"Assignee user {assignee_id} does not exist")


def create_card(db: Session, project_id: int, payload: CardCreate) -> Card:
    """Create a card within a project."""
    get_project(db, project_id)  # ensures project exists (raises otherwise)
    _validate_assignee(db, payload.assignee_id)

    card = Card(
        project_id=project_id,
        title=payload.title,
        description=payload.description,
        status=payload.status,
        assignee_id=payload.assignee_id,
    )
    db.add(card)
    db.commit()
    return _get_card_or_raise(db, card.id)


def list_cards(
    db: Session,
    project_id: int,
    *,
    assignee: str | None = None,
    status: CardStatus | None = None,
) -> list[Card]:
    """List cards in a project, optionally filtered by assignee name and status."""
    # Preserve the existing not-found behaviour for a missing project.
    get_project(db, project_id)   # your existing helper

    stmt = select(Card).where(Card.project_id == project_id)
    if assignee is not None:
        if assignee == "unassigned":
            stmt = stmt.where(Card.assignee_id.is_(None))
        else:
            user = db.scalar(select(User).where(User.name == assignee))
            if user is None:
                raise NotFoundError(f"No user named {assignee!r}")
            stmt = stmt.where(Card.assignee_id == user.id)

    if status is not None:
        stmt = stmt.where(Card.status == status)

    return list(db.scalars(stmt).all())

def get_card(db: Session, card_id: int) -> Card:
    """Return a single card or raise NotFoundError."""
    return _get_card_or_raise(db, card_id)


def update_card(db: Session, card_id: int, payload: CardUpdate) -> Card:
    """Apply a partial update to a card (title, description, status, assignee).

    Because `assignee_id=None` is a legitimate "unassign" instruction, we honour
    explicitly-provided nulls via `exclude_unset`.
    """
    card = _get_card_or_raise(db, card_id)
    data = payload.model_dump(exclude_unset=True)

    if "assignee_id" in data:
        _validate_assignee(db, data["assignee_id"])

    for field, value in data.items():
        setattr(card, field, value)
    db.commit()
    logger.info("Updated card id=%s fields=%s", card_id, list(data))
    return _get_card_or_raise(db, card_id)


def delete_card(db: Session, card_id: int) -> None:
    """Delete a card and its comments/dependency links (via cascade)."""
    card = _get_card_or_raise(db, card_id)
    db.delete(card)
    db.commit()
    logger.info("Deleted card id=%s", card_id)


def get_board(db: Session, project_id: int) -> BoardRead:
    """Assemble the board: cards grouped into columns in status order."""
    cards = list_cards(db, project_id)
    by_status: dict[CardStatus, list[CardRead]] = {status: [] for status in CardStatus.ordered()}
    for card in cards:
        by_status[card.status].append(to_read_model(card))

    columns = [
        BoardColumn(status=status, cards=by_status[status]) for status in CardStatus.ordered()
    ]
    return BoardRead(project_id=project_id, columns=columns)
