from http import HTTPStatus


def test_root_ok(client):
    html = open("src/index.html", encoding="utf-8").read()

    response = client.get("/")

    assert response.status_code == HTTPStatus.OK
    assert response.text == html


def test_user_create_created(client):
    response = client.post(
        "/users/",
        json={"username": "test", "password": "0000"},
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {"id": 1, "username": "test"}


def test_users_read_ok(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {"id": 1, "username": "test"},
        ]
    }


def test_user_read_ok(client):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "username": "test"}


def test_user_read_not_found(client):
    response = client.get("/users/2")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_user_update_ok(client):
    response = client.put(
        "/users/1", json={"username": "t3st", "password": "0000"}
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "username": "t3st"}


def test_user_update_not_found(client):
    response = client.put(
        "/users/2", json={"username": "t3st", "password": "0000"}
    )

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_users_delete_ok(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "username": "t3st"}


def test_users_delete_not_found(client):
    response = client.delete("/users/1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_ws_endpoint(client):
    with client.websocket_connect(url="/ws") as websocket:
        websocket.send_text("hey")
        data = websocket.receive_text()
        assert data == "User says: hey"
