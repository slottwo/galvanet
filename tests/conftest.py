import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import Session

from galvanet.app import app, connections
from galvanet.database import get_session
from galvanet.models import table_registry
from galvanet.settings import Settings


@pytest.fixture
def client(session) -> TestClient:
    
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client
    
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def cleanup_connections() -> None:
    connections.clear()
    yield
    connections.clear()


@pytest.fixture
def session() -> Session:
    # Arrange
    engine = create_engine(
        "sqlite:///:memory",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # Tier down
    table_registry.metadata.drop_all(engine)
