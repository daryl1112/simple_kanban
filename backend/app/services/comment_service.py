"""Business logic for card comments (Markdown bodies)."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models import Comment, User
from app.schemas import CommentCreate
from app.services.card_service import _get_card_or_raise
from app.services.errors import NotFoundError, ValidationError

logger = get_logger(__name__)


def add_comment(db: Session, card_id: int, payload: CommentCreate) -> Comment:
    """Add a Markdown comment to a card, optionally attributed to an author."""
    _get_card_or_raise(db, card_id)  # ensure the card exists

    if payload.author_id is not None and db.get(User, payload.author_id) is None:
        raise ValidationError(f"Author user {payload.author_id} does not exist")

    comment = Comment(card_id=card_id, author_id=payload.author_id, body=payload.body)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    logger.info("Added comment id=%s to card=%s", comment.id, card_id)
    return comment


def list_comments(db: Session, card_id: int) -> list[Comment]:
    """Return a card's comments oldest-first."""
    _get_card_or_raise(db, card_id)
    stmt = select(Comment).where(Comment.card_id == card_id).order_by(Comment.id)
    return list(db.scalars(stmt))


def delete_comment(db: Session, comment_id: int) -> None:
    """Delete a comment by id."""
    comment = db.get(Comment, comment_id)
    if comment is None:
        raise NotFoundError(f"Comment {comment_id} not found")
    db.delete(comment)
    db.commit()
    logger.info("Deleted comment id=%s", comment_id)
