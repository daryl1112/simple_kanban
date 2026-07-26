"""Shared pytest fixtures.

Each test runs against a fresh in-memory SQLite database so tests are isolated
and fast. We override the app's `get_db` dependency to use the test session.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.database import get_db
from app.main import app
from app.models import Base


@pytest.fixture()
def db_session():
    """Provide a clean in-memory database session per test."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # one shared connection for the in-memory DB
    )
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(bind=engine, autoflush=False, autocommit=False)
    session = testing_session()
    try:
        yield session
    finally:
        session.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client(db_session):
    """A TestClient whose requests use the isolated test database."""

    def _override_get_db():
        yield db_session

    app.dependency_overrides[get_db] = _override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()


@pytest.fixture()
def project(client) -> dict:
    """Create and return a project to hang cards off of."""
    resp = client.post("/projects", json={"name": "Test Project", "description": "# Goals"})
    assert resp.status_code == 201
    return resp.json()


@pytest.fixture()
def user(client) -> dict:
    """Create and return a user for assignment tests."""
    resp = client.post("/users", json={"name": "Ada", "email": "ada@example.com"})
    assert resp.status_code == 201
    return resp.json()


def make_card(client, project_id: int, title: str = "Card", **extra) -> dict:
    """Helper to create a card and return its JSON body."""
    body = {"title": title, **extra}
    resp = client.post(f"/projects/{project_id}/cards", json=body)
    assert resp.status_code == 201, resp.text
    return resp.json()
