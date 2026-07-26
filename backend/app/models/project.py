"""Project model. A project owns a single board made up of cards."""

from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base, TimestampMixin


class Project(Base, TimestampMixin):
    """A project. Its cards, grouped by status, form the board."""

    __tablename__ = "projects"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    # Description supports Markdown; stored as raw text and rendered by the UI.
    description: Mapped[str] = mapped_column(default="", nullable=False)

    cards: Mapped[list["Card"]] = relationship(  # noqa: F821
        back_populates="project",
        cascade="all, delete-orphan",
    )
