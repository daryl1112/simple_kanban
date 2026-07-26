"""Declarative base and shared column mixins for ORM models."""

from datetime import datetime, timezone

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


def _utcnow() -> datetime:
    """Return a timezone-aware UTC timestamp (used as a column default)."""
    return datetime.now(timezone.utc)


class Base(DeclarativeBase):
    """Declarative base class that every ORM model inherits from."""


class TimestampMixin:
    """Adds `created_at` / `updated_at` audit columns to a model.

    `updated_at` is refreshed by the database on every UPDATE so callers never
    have to set it manually.
    """

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=_utcnow, onupdate=_utcnow, nullable=False
    )
