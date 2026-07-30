"""Card endpoints: CRUD, creation under a project, plus nested dependency and
comment sub-resources are mounted in their own routers and included here."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.models import CardStatus
from app.api.deps import http_error_from_domain
from app.core.database import get_db
from app.schemas import CardCreate, CardRead, CardUpdate
from app.services import card_service
from app.services.card_service import to_read_model
from app.services.errors import NotFoundError, ValidationError

# Cards are created and listed under a project; individual cards are addressed
# directly by id. Two routers keep the URL structure clean.
project_cards_router = APIRouter(prefix="/projects/{project_id}/cards", tags=["cards"])
cards_router = APIRouter(prefix="/cards", tags=["cards"])


@project_cards_router.post("", response_model=CardRead, status_code=status.HTTP_201_CREATED)
def create_card(project_id: int, payload: CardCreate, db: Session = Depends(get_db)) -> CardRead:
    """Create a card within a project."""
    try:
        card = card_service.create_card(db, project_id, payload)
        return to_read_model(card)
    except (NotFoundError, ValidationError) as exc:
        raise http_error_from_domain(exc) from exc


@project_cards_router.get("", response_model=list[CardRead])
def list_cards(
    project_id: int,
    assignee: str | None = None,
    status: CardStatus | None = None,
    db: Session = Depends(get_db),
) -> list[CardRead]:
    """List cards in a project, optionally filtered by assignee name and/or status."""
    try:
        cards = card_service.list_cards(
            db, project_id, assignee=assignee, status=status
        )
        return [to_read_model(c) for c in cards]
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc


@cards_router.get("/{card_id}", response_model=CardRead)
def get_card(card_id: int, db: Session = Depends(get_db)) -> CardRead:
    """Fetch a single card with its dependencies and comments."""
    try:
        return to_read_model(card_service.get_card(db, card_id))
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc


@cards_router.patch("/{card_id}", response_model=CardRead)
def update_card(card_id: int, payload: CardUpdate, db: Session = Depends(get_db)) -> CardRead:
    """Update a card's title, description, status, or assignee.

    This single endpoint covers moving a card between columns (status) and
    assigning/unassigning it (assignee_id).
    """
    try:
        return to_read_model(card_service.update_card(db, card_id, payload))
    except (NotFoundError, ValidationError) as exc:
        raise http_error_from_domain(exc) from exc


@cards_router.delete("/{card_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_card(card_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a card."""
    try:
        card_service.delete_card(db, card_id)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc
