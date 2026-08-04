"""Checklist and checklist-item models.

A card may have any number of named checklists; each checklist holds a list of
items that can be individually checked off. Both cascade-delete with their
parent so removing a card (or checklist) cleans up everything beneath it.
"""

from sqlalchemy import Boolean, ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Checklist(Base, TimestampMixin):
    """A named task list attached to a card (e.g. "Acceptance criteria")."""

    __tablename__ = "checklists"

    id: Mapped[int] = mapped_column(primary_key=True)
    card_id: Mapped[int] = mapped_column(
        ForeignKey("cards.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(nullable=False)

    items: Mapped[list["ChecklistItem"]] = relationship(
        back_populates="checklist",
        cascade="all, delete-orphan",
        order_by="ChecklistItem.id",
    )
    card: Mapped["Card"] = relationship(back_populates="checklists")  # noqa: F821


class ChecklistItem(Base, TimestampMixin):
    """A single checkable line within a checklist."""

    __tablename__ = "checklist_items"

    id: Mapped[int] = mapped_column(primary_key=True)
    checklist_id: Mapped[int] = mapped_column(
        ForeignKey("checklists.id", ondelete="CASCADE"), nullable=False, index=True
    )
    text: Mapped[str] = mapped_column(Text, nullable=False)
    is_completed: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

    checklist: Mapped["Checklist"] = relationship(back_populates="items")
