"""Centralised logging configuration.

We configure logging in one place so every module gets consistent, structured
output. Modules obtain a logger via `get_logger(__name__)` rather than calling
`logging.basicConfig` themselves.
"""

import logging
import sys

from app.core.config import get_settings

_CONFIGURED = False
_LOG_FORMAT = "%(asctime)s | %(levelname)-8s | %(name)s | %(message)s"


def configure_logging() -> None:
    """Configure the root logger exactly once.

    Idempotent: repeated calls (e.g. from tests) are no-ops after the first,
    which prevents duplicate handlers from stacking up.
    """
    global _CONFIGURED
    if _CONFIGURED:
        return

    settings = get_settings()
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT))

    root = logging.getLogger()
    root.setLevel(settings.log_level.upper())
    root.handlers.clear()
    root.addHandler(handler)

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a module logger, ensuring logging is configured first."""
    configure_logging()
    return logging.getLogger(name)
