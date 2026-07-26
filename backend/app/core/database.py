"""Database engine and session management.

Exposes a configured SQLAlchemy engine, a session factory, and a `get_db`
generator used by the API layer for per-request sessions. Keeping this in one
module means the rest of the app never touches engine construction directly.
"""

from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.core.config import get_settings
from app.core.logging import get_logger

logger = get_logger(__name__)

settings = get_settings()

# SQLite needs a special flag when used across threads (FastAPI's threadpool);
# other engines (Postgres) ignore the connect_args below.
_connect_args = (
    {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)

engine = create_engine(settings.database_url, connect_args=_connect_args, future=True)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)


def get_db() -> Iterator[Session]:
    """Yield a database session and guarantee it is closed afterwards.

    Used as a FastAPI dependency so each request gets its own session that is
    cleanly released once the request completes.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
