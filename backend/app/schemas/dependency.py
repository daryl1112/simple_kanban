"""Request schemas for card dependencies."""

from pydantic import BaseModel, Field


class DependencyCreate(BaseModel):
    """Declare that a card depends on another card."""

    depends_on_id: int = Field(description="Id of the card that must come first")
