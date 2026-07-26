"""The set of columns (statuses) a card can occupy on a board.

Defined once here and reused by the model, schemas, and services so the
allowed values never drift apart.
"""

from enum import Enum


class CardStatus(str, Enum):
    """Workflow columns for a card, in board order."""

    BACKLOG = "backlog"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    COMPLETED = "completed"

    @classmethod
    def ordered(cls) -> list["CardStatus"]:
        """Return statuses in their natural left-to-right board order."""
        return [cls.BACKLOG, cls.APPROVED, cls.IN_PROGRESS, cls.REVIEW, cls.COMPLETED]
