"""FastAPI application entrypoint.

Wires together configuration, logging, the database schema, CORS, a request
logging middleware, and every API router. Import `app` to run with uvicorn:

    uvicorn app.main:app --host 0.0.0.0 --port 8000
"""

import time

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import all_routers
from app.core.config import get_settings
from app.core.database import engine
from app.core.logging import configure_logging, get_logger
from app.models import Base

configure_logging()
logger = get_logger(__name__)
settings = get_settings()


def create_app() -> FastAPI:
    """Build and configure the FastAPI application (factory pattern)."""
    application = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description=(
            "In-house Kanban board API. Every board action — projects, cards, "
            "dependencies, assignment, and Markdown comments — is available here."
        ),
    )

    # Create tables on startup. For a small in-house tool this is sufficient;
    # a larger deployment would use Alembic migrations instead.
    Base.metadata.create_all(bind=engine)

    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @application.middleware("http")
    async def log_requests(request: Request, call_next):
        """Log each request's method, path, status, and duration."""
        start = time.perf_counter()
        response = await call_next(request)
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "%s %s -> %s (%.1f ms)",
            request.method,
            request.url.path,
            response.status_code,
            elapsed_ms,
        )
        return response

    @application.get("/health", tags=["system"])
    def health() -> dict[str, str]:
        """Liveness probe used by Docker Compose's health check."""
        return {"status": "ok"}

    for router in all_routers:
        application.include_router(router)

    logger.info("%s initialised with %d routers", settings.app_name, len(all_routers))
    return application


app = create_app()
