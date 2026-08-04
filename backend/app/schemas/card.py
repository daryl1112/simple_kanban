"""Request/response schemas for cards, including board grouping."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, computed_field

from app.models.card_status import CardStatus
from app.schemas.checklist import ChecklistRead
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
    checklists: list[ChecklistRead] = []
    created_at: datetime
    updated_at: datetime

    @computed_field  # total checklist items across the card (board badge denominator)
    @property
    def checklist_items_total(self) -> int:
        return sum(len(cl.items) for cl in self.checklists)

    @computed_field  # completed checklist items across the card (badge numerator)
    @property
    def checklist_items_completed(self) -> int:
        return sum(
            1 for cl in self.checklists for item in cl.items if item.is_completed
        )


class BoardColumn(BaseModel):
    """A single status column on the board and the cards within it."""

    status: CardStatus
    cards: list[CardRead]


class BoardRead(BaseModel):
    """A project's board: every status column in board order."""

    project_id: int
    columns: list[BoardColumn]
