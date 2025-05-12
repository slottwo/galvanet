from jwt import decode

from galvanet.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {"sub": "test"}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, [ALGORITHM])

    assert decoded["sub"] == data["sub"]
    assert decoded["exp"]
