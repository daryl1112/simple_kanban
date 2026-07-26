"""Business logic for projects."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.logging import get_logger
from app.models import Project
from app.schemas import ProjectCreate, ProjectUpdate
from app.services.errors import NotFoundError

logger = get_logger(__name__)


def create_project(db: Session, payload: ProjectCreate) -> Project:
    """Create and persist a new project."""
    project = Project(name=payload.name, description=payload.description)
    db.add(project)
    db.commit()
    db.refresh(project)
    logger.info("Created project id=%s name=%s", project.id, project.name)
    return project


def list_projects(db: Session) -> list[Project]:
    """Return all projects ordered by id."""
    return list(db.scalars(select(Project).order_by(Project.id)))


def get_project(db: Session, project_id: int) -> Project:
    """Return a single project or raise NotFoundError."""
    project = db.get(Project, project_id)
    if project is None:
        raise NotFoundError(f"Project {project_id} not found")
    return project


def update_project(db: Session, project_id: int, payload: ProjectUpdate) -> Project:
    """Apply a partial update to a project."""
    project = get_project(db, project_id)
    data = payload.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(project, field, value)
    db.commit()
    db.refresh(project)
    logger.info("Updated project id=%s fields=%s", project_id, list(data))
    return project


def delete_project(db: Session, project_id: int) -> None:
    """Delete a project and, by cascade, its cards and comments."""
    project = get_project(db, project_id)
    db.delete(project)
    db.commit()
    logger.info("Deleted project id=%s", project_id)
