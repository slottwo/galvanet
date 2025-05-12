from http import HTTPStatus

from galvanet.schemas import UserPublic


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


def test_user_create_conflict(client, user):
    response = client.post(
        "/users/",
        json={"username": "test", "password": "0000"},
    )

    assert response.status_code == HTTPStatus.CONFLICT
    assert response.json() == {"detail": "Username already exists"}


def test_users_read_ok(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": []}


def test_users_read_with_users_ok(client, user):
    user_public = UserPublic.model_validate(user).model_dump()

    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"users": [user_public]}


def test_user_read_ok(client, user):
    user_public = UserPublic.model_validate(user).model_dump()

    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_public


def test_user_read_not_found(client):
    response = client.get("/users/1")

    assert response.status_code == HTTPStatus.NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_user_update_ok(client, user, token):
    response = client.put(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "t3st", "password": "password"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"id": 1, "username": "t3st"}


def test_user_update_forbidden(client, user, token):
    response = client.put(
        f"/users/{user.id + 1}",
        headers={"Authorization": f"Bearer {token}"},
        json={"username": "t3st", "password": "password"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}


def test_users_delete_ok(client, user, token):
    user_public = UserPublic.model_validate(user).model_dump()

    response = client.delete(
        f"/users/{user.id}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.OK
    assert response.json() == user_public


def test_users_delete_forbidden(client, user, token):
    response = client.delete(
        f"/users/{user.id + 1}",
        headers={"Authorization": f"Bearer {token}"},
    )

    assert response.status_code == HTTPStatus.FORBIDDEN
    assert response.json() == {"detail": "Not enough permissions"}


def test_get_token_ok(client, user):
    response = client.post(
        "/token",
        data={"username": user.username, "password": user.plain_password},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.OK
    assert token["token_type"] == "Bearer"
    assert token["access_token"]


def test_get_token_bad_request(client, user):
    response = client.post(
        "/token",
        data={"username": user.username, "password": "invalid-password"},
    )

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert response.json() == {"detail": "Invalid credentials"}


def test_ws_chat(client):
    with client.websocket_connect(url="/ws/chat") as websocket:
        websocket.send_text("hey")
        data = websocket.receive_text()
        assert data == "hey"
