import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from galvanet.app import app, connections
from galvanet.database import get_session
from galvanet.models import User, table_registry
from galvanet.security import pwd_hash


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
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    table_registry.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

    # Tier down
    table_registry.metadata.drop_all(engine)


@pytest.fixture
def user(session) -> User:
    pwd = "password"

    user = User(username="test", password=pwd_hash(pwd))

    session.add(user)
    session.commit()
    session.refresh(user)

    user.plain_password = pwd  # Monkey Patch

    return user


@pytest.fixture
def token(client, user) -> str:
    response = client.post(
        "/token",
        data={"username": user.username, "password": user.plain_password},
    )
    return response.json()["access_token"]
