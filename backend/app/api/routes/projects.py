"""Project endpoints, including the assembled board view."""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.api.deps import http_error_from_domain
from app.core.database import get_db
from app.schemas import ProjectCreate, ProjectRead, ProjectUpdate
from app.schemas.card import BoardRead
from app.services import card_service, project_service
from app.services.errors import NotFoundError

router = APIRouter(prefix="/projects", tags=["projects"])


@router.post("", response_model=ProjectRead, status_code=status.HTTP_201_CREATED)
def create_project(payload: ProjectCreate, db: Session = Depends(get_db)) -> ProjectRead:
    """Create a project (description supports Markdown)."""
    return project_service.create_project(db, payload)


@router.get("", response_model=list[ProjectRead])
def list_projects(db: Session = Depends(get_db)) -> list[ProjectRead]:
    """List all projects."""
    return project_service.list_projects(db)


@router.get("/{project_id}", response_model=ProjectRead)
def get_project(project_id: int, db: Session = Depends(get_db)) -> ProjectRead:
    """Fetch a single project."""
    try:
        return project_service.get_project(db, project_id)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc


@router.patch("/{project_id}", response_model=ProjectRead)
def update_project(
    project_id: int, payload: ProjectUpdate, db: Session = Depends(get_db)
) -> ProjectRead:
    """Partially update a project."""
    try:
        return project_service.update_project(db, project_id, payload)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int, db: Session = Depends(get_db)) -> None:
    """Delete a project and its board."""
    try:
        project_service.delete_project(db, project_id)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc


@router.get("/{project_id}/board", response_model=BoardRead)
def get_board(project_id: int, db: Session = Depends(get_db)) -> BoardRead:
    """Return the project's board: cards grouped by status column."""
    try:
        return card_service.get_board(db, project_id)
    except NotFoundError as exc:
        raise http_error_from_domain(exc) from exc
