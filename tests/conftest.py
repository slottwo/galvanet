import pytest
from fastapi.testclient import TestClient

from galvanet.app import app


@pytest.fixture
def client():
    return TestClient(app)
