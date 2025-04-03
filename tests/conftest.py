import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from galvanet.app import app
from galvanet.models import table_registry
from galvanet.settings import Settings


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def session():
    # Arrange
    engine = create_engine(Settings().DATABASE_URL)
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # Tier down
    table_registry.metadata.drop_all(engine)
