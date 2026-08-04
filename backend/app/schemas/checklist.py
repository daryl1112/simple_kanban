"""Request/response schemas for checklists and their items."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, computed_field


class ChecklistItemCreate(BaseModel):
    """Payload for adding an item to a checklist (plain text)."""

    text: str = Field(min_length=1, max_length=500)
    is_completed: bool = False


class ChecklistItemUpdate(BaseModel):
    """Payload for editing an item's text and/or toggling completion."""

    text: str | None = Field(default=None, min_length=1, max_length=500)
    is_completed: bool | None = None


class ChecklistItemRead(BaseModel):
    """A checklist item as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    checklist_id: int
    text: str
    is_completed: bool
    created_at: datetime
    updated_at: datetime


class ChecklistCreate(BaseModel):
    """Payload for creating a checklist on a card."""

    title: str = Field(min_length=1, max_length=200)


class ChecklistUpdate(BaseModel):
    """Payload for renaming a checklist."""

    title: str | None = Field(default=None, min_length=1, max_length=200)


class ChecklistRead(BaseModel):
    """A checklist with its items and derived progress counts."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    card_id: int
    title: str
    items: list[ChecklistItemRead] = []
    created_at: datetime
    updated_at: datetime

    @computed_field  # progress numerator, derived from items
    @property
    def completed_count(self) -> int:
        return sum(1 for item in self.items if item.is_completed)

    @computed_field  # progress denominator
    @property
    def total_count(self) -> int:
        return len(self.items)
