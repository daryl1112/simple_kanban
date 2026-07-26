"""User model. Users exist so that cards can be assigned to someone.

This is an in-house tool with no authentication; a user is simply a named
person a card can be assigned to.
"""

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class User(Base, TimestampMixin):
    """A person who can be assigned to cards and author comments."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False, index=True)

    assigned_cards: Mapped[list["Card"]] = relationship(  # noqa: F821
        back_populates="assignee"
    )
