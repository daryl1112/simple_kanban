"""Card dependency endpoints (nested under a card)."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import http_error_from_domain
from app.core.database import get_db
from app.schemas import CardRead, DependencyCreate
from app.services import dependency_service
from app.services.card_service import to_read_model
from app.services.errors import NotFoundError, ValidationError

router = APIRouter(prefix="/cards/{card_id}/dependencies", tags=["dependencies"])


@router.post("", response_model=CardRead, status_code=status.HTTP_201_CREATED)
def add_dependency(
    card_id: int, payload: DependencyCreate, db: Session = Depends(get_db)
) -> CardRead:
    """Declare that this card depends on another card (cycle-checked)."""
    try:
        card = dependency_service.add_dependency(db, card_id, payload.depends_on_id)
        return to_read_model(card)
    except (NotFoundError, ValidationError) as exc:
        raise http_error_from_domain(exc) from exc


@router.get("", response_model=list[CardRead])
def list_dependencies(card_id: int, db: Session = Depends(get_db)) -> list[CardRead]:
    """List the cards this card depends on."""
    try:
        return [to_read_model(c) for c in dependency_service.list_dependencies(db, card_id)]
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc


@router.delete("/{depends_on_id}", response_model=CardRead)
def remove_dependency(
    card_id: int, depends_on_id: int, db: Session = Depends(get_db)
) -> CardRead:
    """Remove a dependency edge from this card."""
    try:
        card = dependency_service.remove_dependency(db, card_id, depends_on_id)
        return to_read_model(card)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc
