"""Request/response schemas for cards, including board grouping."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.card_status import CardStatus
from app.schemas.comment import CommentRead


class CardCreate(BaseModel):
    """Payload for creating a card. `description` accepts Markdown."""

    title: str = Field(min_length=1, max_length=300)
    description: str = Field(default="", description="Markdown-formatted description")
    status: CardStatus = CardStatus.BACKLOG
    assignee_id: int | None = None


class CardUpdate(BaseModel):
    """Payload for partially updating a card.

    Any subset of fields may be supplied; omitted fields are left unchanged.
    Setting `assignee_id` to null unassigns the card.
    """

    title: str | None = Field(default=None, min_length=1, max_length=300)
    description: str | None = Field(default=None, description="Markdown-formatted description")
    status: CardStatus | None = None
    assignee_id: int | None = None


class CardRead(BaseModel):
    """Card as returned by the API, with dependency ids and comments."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    project_id: int
    title: str
    description: str
    status: CardStatus
    assignee_id: int | None
    dependency_ids: list[int] = []
    comments: list[CommentRead] = []
    created_at: datetime
    updated_at: datetime


class BoardColumn(BaseModel):
    """A single status column on the board and the cards within it."""

    status: CardStatus
    cards: list[CardRead]


class BoardRead(BaseModel):
    """A project's board: every status column in board order."""

    project_id: int
    columns: list[BoardColumn]
