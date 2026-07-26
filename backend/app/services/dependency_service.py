"""Business logic for card dependencies, with cycle prevention.

A dependency is a directed edge "card depends on depends_on". The dependency
graph must remain a DAG, so before adding an edge we verify it would not
introduce a cycle.
"""

from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models import Card
from app.services.card_service import _get_card_or_raise
from app.services.errors import ValidationError

logger = get_logger(__name__)


def _would_create_cycle(source: Card, target: Card) -> bool:
    """Return True if adding "source depends on target" would form a cycle.

    Adding the edge source -> target creates a cycle iff `source` is already
    reachable from `target` by following existing dependency edges. We walk the
    graph from `target` with an iterative depth-first search.
    """
    stack = [target]
    seen: set[int] = set()
    while stack:
        current = stack.pop()
        if current.id == source.id:
            return True
        if current.id in seen:
            continue
        seen.add(current.id)
        stack.extend(current.dependencies)
    return False


def add_dependency(db: Session, card_id: int, depends_on_id: int) -> Card:
    """Declare that `card_id` depends on `depends_on_id`.

    Validates that: the two cards differ, both exist, they belong to the same
    project, and the new edge introduces no cycle. Idempotent — re-adding an
    existing dependency is a no-op.
    """
    if card_id == depends_on_id:
        raise ValidationError("A card cannot depend on itself")

    card = _get_card_or_raise(db, card_id)
    target = _get_card_or_raise(db, depends_on_id)

    if card.project_id != target.project_id:
        raise ValidationError("Dependencies must be between cards in the same project")

    if target in card.dependencies:
        return card  # already present; nothing to do

    if _would_create_cycle(card, target):
        raise ValidationError(
            f"Adding dependency {card_id} -> {depends_on_id} would create a cycle"
        )

    card.dependencies.append(target)
    db.commit()
    logger.info("Added dependency card=%s depends_on=%s", card_id, depends_on_id)
    return _get_card_or_raise(db, card_id)


def remove_dependency(db: Session, card_id: int, depends_on_id: int) -> Card:
    """Remove the dependency edge `card_id` -> `depends_on_id` if it exists."""
    card = _get_card_or_raise(db, card_id)
    target = _get_card_or_raise(db, depends_on_id)

    if target in card.dependencies:
        card.dependencies.remove(target)
        db.commit()
        logger.info("Removed dependency card=%s depends_on=%s", card_id, depends_on_id)
    return _get_card_or_raise(db, card_id)


def list_dependencies(db: Session, card_id: int) -> list[Card]:
    """Return the cards a given card depends on."""
    card = _get_card_or_raise(db, card_id)
    return list(card.dependencies)
