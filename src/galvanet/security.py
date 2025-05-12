from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from jwt import encode
from pwdlib import PasswordHash
from sqlalchemy.orm import Session

from galvanet.database import get_session

pwd_context = PasswordHash.recommended()

SECRET_KEY = "bumbum"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")


def pwd_hash(plain_pwd: str) -> str:  # pragma: no cover
    return pwd_context.hash(plain_pwd)


def pwd_check(plain_pwd: str, hashed_pwd: str) -> bool:  # pragma: no cover
    return pwd_context.verify(plain_pwd, hashed_pwd)


def create_access_token(payload: dict) -> str:
    to_encode = payload.copy()

    expire_at = datetime.now(tz=ZoneInfo("UTC")) + timedelta(
        minutes=ACCESS_TOKEN_EXPIRE_MINUTES
    )

    to_encode.update({"exp": expire_at})

    encoded_jwt = encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt


def get_current_user(
    session: Session = Depends(get_session),
    token: str = Depends(oauth2_schema),
): ...
