"""Route barrel: exposes every router for registration in `main`."""

from app.api.routes.cards import cards_router, project_cards_router
from app.api.routes.comments import card_comments_router, comments_router
from app.api.routes.dependencies import router as dependencies_router
from app.api.routes.projects import router as projects_router
from app.api.routes.users import router as users_router

# Ordered list of every router the application exposes.
all_routers = [
    projects_router,
    project_cards_router,
    cards_router,
    dependencies_router,
    card_comments_router,
    comments_router,
    users_router,
]

__all__ = ["all_routers"]
