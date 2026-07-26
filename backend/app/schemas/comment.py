"""Request/response schemas for comments."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CommentCreate(BaseModel):
    """Payload for adding a comment. `body` accepts Markdown."""

    body: str = Field(min_length=1, description="Markdown-formatted comment body")
    author_id: int | None = Field(default=None, description="Optional author user id")


class CommentRead(BaseModel):
    """Comment as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    card_id: int
    author_id: int | None
    body: str
    created_at: datetime
    updated_at: datetime
