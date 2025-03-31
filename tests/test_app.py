from fastapi.testclient import TestClient

from galvanet.app import app

client = TestClient(app)
