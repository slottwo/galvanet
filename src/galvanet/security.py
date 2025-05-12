from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from jwt import encode
from pwdlib import PasswordHash

pwd_context = PasswordHash.recommended()

SECRET_KEY = "bumbum"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def pwd_hash(plain_pwd: str) -> str:  # pragma: no cover
    return pwd_context.hash(plain_pwd)


def pwd_check(plain_pwd: str, hashed_pwd: str) -> bool:  # pragma: no cover
    return pwd_context.verify(plain_pwd, hashed_pwd)


def create_access_token(payload: dict) -> str:
    to_encode = payload.copy()

    expire_at = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({'exp': expire_at})

    encoded_jwt = encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt
