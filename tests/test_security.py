from http import HTTPStatus

from jwt import decode

from galvanet.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {"sub": "test"}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, [ALGORITHM])

    assert decoded["sub"] == data["sub"]
    assert decoded["exp"]


def test_jwt_invalid_token(client):
    response = client.delete(
        "/users/1", headers={"Authorization": "Bearer token-invalido"}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {"detail": "Could not validate credentials"}


# def test_jwt_invalid_token_without_sub(client):

def test_get_current_user_not_found(client):
    data = {'nobody': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {'detail': 'Could not validate credentials'}


def test_get_current_user_does_not_exists(client):
    data = {'sub': 'test'}
    token = create_access_token(data)

    response = client.delete(
        '/users/1',
        headers={'Authorization': f'Bearer {token}'},
    )
