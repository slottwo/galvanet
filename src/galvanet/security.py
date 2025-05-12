from datetime import datetime, timedelta
from http import HTTPStatus
from zoneinfo import ZoneInfo

from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jwt import PyJWTError, decode, encode
from pwdlib import PasswordHash
from sqlalchemy import select
from sqlalchemy.orm import Session

from galvanet.database import get_session
from galvanet.models import User
from galvanet.settings import Settings

pwd_context = PasswordHash.recommended()

SECRET_KEY = Settings().SECRET_KEY
ALGORITHM = Settings().TOKEN_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = Settings().ACCESS_TOKEN_EXPIRE_MINUTES

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
):
    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(token, SECRET_KEY, [ALGORITHM])

        if not payload.get("sub"):
            raise credentials_exception
    except PyJWTError:
        raise credentials_exception

    user_db = session.scalar(
        select(User).where(User.username == payload.get("sub"))
    )

    if not user_db:
        raise credentials_exception

    return user_db
