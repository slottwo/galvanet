from http import HTTPStatus


def test_root_ok(client):
    # Arrange
    html = open("src/index.html", encoding="utf-8").read()

    # Act
    response = client.get("/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.text == html


def test_users_create(client):
    # Act
    response = client.post(
        "/users/",
        json={"username": "testusername", "password": "testpassword"},
    )

    # Assert
    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id": 1, "username": "testusername"}


def test_users_read(client):
    # Act
    response = client.get("/users/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {"id": 1, "username": "testusername"},
        ]
    }


# def test_ws_endpoint(client: TestClient):
#     # Act
#     client.websocket_connect()
