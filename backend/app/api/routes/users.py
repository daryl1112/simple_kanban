"""User endpoints."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import http_error_from_domain
from app.core.database import get_db
from app.schemas import UserCreate, UserRead, UserUpdate
from app.services import user_service
from app.services.errors import NotFoundError, ValidationError

router = APIRouter(prefix="/users", tags=["users"])


@router.post("", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, db: Session = Depends(get_db)) -> UserRead:
    """Create a user (a person cards can be assigned to)."""
    try:
        return user_service.create_user(db, payload)
    except ValidationError as exc:
        raise http_error_from_domain(exc) from exc


@router.get("", response_model=list[UserRead])
def list_users(
    email: str | None = None,
    db: Session = Depends(get_db),
) -> list[UserRead]:
    """List users, optionally filtered by exact email."""
    if email is not None:
        try:
            return [user_service.get_user_by_email(db, email)]
        except NotFoundError:
            return []
    return user_service.list_users(db)


@router.get("/{user_id}", response_model=UserRead)
def get_user(user_id: int, db: Session = Depends(get_db)) -> UserRead:
    """Fetch a single user."""
    try:
        return user_service.get_user(db, user_id)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc

@router.patch("/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)) -> UserRead:
    """Partially update a user."""
    try:
        return user_service.update_user(db, user_id, payload)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a user."""
    try:
        user_service.delete_user(db, user_id)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc
