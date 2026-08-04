"""Checklist and checklist-item endpoints.

Checklists are created/listed under a card; individual checklists are addressed
by id; items are added under a checklist and edited/deleted by their own id.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import http_error_from_domain
from app.core.database import get_db
from app.schemas import (
    ChecklistCreate,
    ChecklistItemCreate,
    ChecklistItemRead,
    ChecklistItemUpdate,
    ChecklistRead,
    ChecklistUpdate,
)
from app.services import checklist_service
from app.services.errors import NotFoundError, ValidationError

# Checklists nested under a card, checklists by id, and items by id.
card_checklists_router = APIRouter(prefix="/cards/{card_id}/checklists", tags=["checklists"])
checklists_router = APIRouter(prefix="/checklists", tags=["checklists"])
checklist_items_router = APIRouter(prefix="/checklist-items", tags=["checklists"])


@card_checklists_router.post("", response_model=ChecklistRead, status_code=status.HTTP_201_CREATED)
def create_checklist(
    card_id: int, payload: ChecklistCreate, db: Session = Depends(get_db)
) -> ChecklistRead:
    """Create a checklist on a card."""
    try:
        return checklist_service.create_checklist(db, card_id, payload)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc


@card_checklists_router.get("", response_model=list[ChecklistRead])
def list_checklists(card_id: int, db: Session = Depends(get_db)) -> list[ChecklistRead]:
    """List a card's checklists."""
    try:
        return checklist_service.list_checklists(db, card_id)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc


@checklists_router.patch("/{checklist_id}", response_model=ChecklistRead)
def update_checklist(
    checklist_id: int, payload: ChecklistUpdate, db: Session = Depends(get_db)
) -> ChecklistRead:
    """Rename a checklist."""
    try:
        return checklist_service.update_checklist(db, checklist_id, payload)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc


@checklists_router.delete("/{checklist_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_checklist(checklist_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a checklist and all of its items."""
    try:
        checklist_service.delete_checklist(db, checklist_id)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc


@checklists_router.post(
    "/{checklist_id}/items", response_model=ChecklistItemRead, status_code=status.HTTP_201_CREATED
)
def add_item(
    checklist_id: int, payload: ChecklistItemCreate, db: Session = Depends(get_db)
) -> ChecklistItemRead:
    """Add an item to a checklist."""
    try:
        return checklist_service.add_item(db, checklist_id, payload)
    except (NotFoundError, ValidationError) as exc:
        raise http_error_from_domain(exc) from exc


@checklist_items_router.patch("/{item_id}", response_model=ChecklistItemRead)
def update_item(
    item_id: int, payload: ChecklistItemUpdate, db: Session = Depends(get_db)
) -> ChecklistItemRead:
    """Edit an item's text or toggle whether it's completed."""
    try:
        return checklist_service.update_item(db, item_id, payload)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc


@checklist_items_router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(item_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a single checklist item."""
    try:
        checklist_service.delete_item(db, item_id)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc
