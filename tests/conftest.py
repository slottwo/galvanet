import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from galvanet.app import app, connections
from galvanet.models import table_registry
from galvanet.settings import Settings


@pytest.fixture
def client() -> TestClient:
    return TestClient(app)


@pytest.fixture(autouse=True)
def cleanup_connections():
    connections.clear()
    yield
    connections.clear()


@pytest.fixture
def session() -> Session:
    # Arrange
    engine = create_engine(Settings().DATABASE_URL)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # Tier down
    table_registry.metadata.drop_all(engine)
