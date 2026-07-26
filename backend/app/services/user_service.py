"""Business logic for users.

Each function has a single responsibility and operates on a SQLAlchemy session
passed in by the caller, keeping the service free of request/HTTP concerns.
"""

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models import User
from app.schemas import UserCreate, UserUpdate
from app.services.errors import NotFoundError, ValidationError

logger = get_logger(__name__)


def create_user(db: Session, payload: UserCreate) -> User:
    """Create and persist a new user."""
    user = User(name=payload.name, email=payload.email)
    db.add(user)
    try:
        db.commit()
    except IntegrityError as exc:
        # The email column is unique; a clash is a client error, not a 500.
        db.rollback()
        raise ValidationError(f"A user with email {payload.email} already exists") from exc
    db.refresh(user)
    logger.info("Created user id=%s email=%s", user.id, user.email)
    return user


def list_users(db: Session) -> list[User]:
    """Return all users ordered by id."""
    return list(db.scalars(select(User).order_by(User.id)))


def get_user(db: Session, user_id: int) -> User:
    """Return a single user or raise NotFoundError."""
    user = db.get(User, user_id)
    if user is None:
        raise NotFoundError(f"User {user_id} not found")
    return user


def update_user(db: Session, user_id: int, payload: UserUpdate) -> User:
    """Apply a partial update to a user."""
    user = get_user(db, user_id)
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    logger.info("Updated user id=%s fields=%s", user_id, list(data))
    return user


def delete_user(db: Session, user_id: int) -> None:
    """Delete a user. Assigned cards are unassigned via the FK ON DELETE."""
    user = get_user(db, user_id)
    db.delete(user)
    db.commit()
    logger.info("Deleted user id=%s", user_id)
