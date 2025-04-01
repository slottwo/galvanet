from http import HTTPStatus

from fastapi.testclient import TestClient

from galvanet.app import app


def test_root_ok():
    # Arrange
    html = open("src/index.html", encoding="utf-8").read()
    client = TestClient(app)

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.text == html
