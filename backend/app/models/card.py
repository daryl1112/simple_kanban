"""Card model plus the self-referential dependency association table.

A card belongs to a project, sits in exactly one status column, may be
assigned to a user, and may depend on any number of other cards. Dependencies
are modelled as a many-to-many self-join through `card_dependencies`.
"""

from sqlalchemy import Column, ForeignKey, Integer, Table, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin
from app.models.card_status import CardStatus

# Association table: (card_id) depends on (depends_on_id).
card_dependencies = Table(
    "card_dependencies",
    Base.metadata,
    Column("card_id", Integer, ForeignKey("cards.id", ondelete="CASCADE"), primary_key=True),
    Column(
        "depends_on_id",
        Integer,
        ForeignKey("cards.id", ondelete="CASCADE"),
        primary_key=True,
    ),
)


class Card(Base, TimestampMixin):
    """A unit of work on a project's board."""

    __tablename__ = "cards"

    id: Mapped[int] = mapped_column(primary_key=True)
    project_id: Mapped[int] = mapped_column(
        ForeignKey("projects.id", ondelete="CASCADE"), nullable=False, index=True
    )
    title: Mapped[str] = mapped_column(nullable=False)
    # Description supports Markdown; stored raw, rendered by the UI.
    description: Mapped[str] = mapped_column(Text, default="", nullable=False)
    status: Mapped[CardStatus] = mapped_column(default=CardStatus.BACKLOG, nullable=False)
    assignee_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id", ondelete="SET NULL"), nullable=True
    )

    project: Mapped["Project"] = relationship(back_populates="cards")  # noqa: F821
    assignee: Mapped["User | None"] = relationship(back_populates="assigned_cards")  # noqa: F821
    comments: Mapped[list["Comment"]] = relationship(  # noqa: F821
        back_populates="card", cascade="all, delete-orphan"
    )

    # Cards this card depends on (outgoing edges in the dependency graph).
    dependencies: Mapped[list["Card"]] = relationship(
        "Card",
        secondary=card_dependencies,
        primaryjoin=id == card_dependencies.c.card_id,
        secondaryjoin=id == card_dependencies.c.depends_on_id,
        backref="dependents",
    )
