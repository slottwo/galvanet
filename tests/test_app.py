from http import HTTPStatus

from fastapi.testclient import TestClient


def test_root_ok(client: TestClient):
    # Arrange
    html = open("src/index.html", encoding="utf-8").read()

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.text == html


def test_users_create(client: TestClient):
    # Act
    response = client.post(
        "/users/",
        json={"username": "testusername", "password": "testpassword"},
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id": 1, "username": "testusername"}


"""
def test_ws_endpoint(client: TestClient):
    # Act
    client.websocket_connect"""
