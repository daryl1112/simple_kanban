"""Request/response schemas for projects."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class ProjectCreate(BaseModel):
    """Payload for creating a project. `description` accepts Markdown."""

    name: str = Field(min_length=1, max_length=200)
    description: str = Field(default="", description="Markdown-formatted description")


class ProjectUpdate(BaseModel):
    """Payload for partially updating a project."""

    name: str | None = Field(default=None, min_length=1, max_length=200)
    description: str | None = Field(default=None, description="Markdown-formatted description")


class ProjectRead(BaseModel):
    """Project as returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str
    created_at: datetime
    updated_at: datetime
