"""Comment model. Comments are threaded under a card and support Markdown."""

from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Comment(Base, TimestampMixin):
    """A Markdown comment left on a card, optionally attributed to a user."""

    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(
        ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True
    )
    author_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )
    # Body supports Markdown; stored raw, rendered by the UI.
    body: Mapped[str] = mapped_column(Text, nullable=False)

    author: Mapped["User | None"] = relationship()  # noqa: F821
    card: Mapped["Card"] = relationship(back_populates="comments")  # noqa: F821
