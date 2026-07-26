"""Comment endpoints (nested under a card, plus direct delete by id)."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import http_error_from_domain
from app.core.database import get_db
from app.schemas import CommentCreate, CommentRead
from app.services import comment_service
from app.services.errors import NotFoundError, ValidationError

card_comments_router = APIRouter(prefix="/cards/{card_id}/comments", tags=["comments"])
comments_router = APIRouter(prefix="/comments", tags=["comments"])


@card_comments_router.post("", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def add_comment(card_id: int, payload: CommentCreate, db: Session = Depends(get_db)) -> CommentRead:
    """Add a Markdown comment to a card."""
    try:
        return comment_service.add_comment(db, card_id, payload)
    except (NotFoundError, ValidationError) as exc:
        raise http_error_from_domain(exc) from exc


@card_comments_router.get("", response_model=list[CommentRead])
def list_comments(card_id: int, db: Session = Depends(get_db)) -> list[CommentRead]:
    """List a card's comments (oldest first)."""
    try:
        return comment_service.list_comments(db, card_id)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc


@comments_router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a comment by id."""
    try:
        comment_service.delete_comment(db, comment_id)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc
