from http import HTTPStatus

from fastapi import (
    Depends,
    FastAPI,
    HTTPException,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from galvanet.database import get_session
from galvanet.models import User
from galvanet.schemas import Token, UserList, UserPublic, UserSchema
from galvanet.security import pwd_check, pwd_hash, create_access_token

# Application
app = FastAPI()

# List to store connected only-chatting clients
connections: list[WebSocket] = []

# List to store running games and it connected clients
active_games = {}  # game_id: str, websockets: list[str]

# HTTP endpoints:


@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("src/index.html", encoding="utf-8") as file:
        return HTMLResponse(file.read())


@app.get("/users/", response_model=UserList)
def read_users(
    limit: int = 10, offset: int = 0, session: Session = Depends(get_session)
):
    users_db = session.scalars(select(User).limit(limit).offset(offset))
    return {"users": users_db}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema, session: Session = Depends(get_session)):
    if session.scalar(select(User).where(User.username == user.username)):
        raise HTTPException(
            status_code=HTTPStatus.CONFLICT,
            detail="Username already exists",
        )

    user_db = User(username=user.username, password=pwd_hash(user.password))

    session.add(user_db)
    session.commit()
    session.refresh(user_db)

    return user_db


@app.get("/users/{user_id}", response_model=UserPublic)
def read_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if user_db:
        return user_db

    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="User not found"
    )


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(
    user_id: int, user: UserSchema, session: Session = Depends(get_session)
):
    user_db: User = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    user_db.username = user.username
    user_db.password = pwd_hash(user.password)

    session.commit()
    session.refresh(user_db)

    return user_db


@app.delete("/users/{user_id}", response_model=UserPublic)
def delete_user(user_id: int, session: Session = Depends(get_session)):
    user_db = session.scalar(select(User).where(User.id == user_id))

    if not user_db:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    session.delete(user_db)
    session.commit()

    return user_db


@app.post("/token", response_model=Token)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    user_db = session.scalar(
        select(User).where(User.username == form_data.username)
    )

    if not user_db and not pwd_check(form_data.password, user_db.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST, detail="Invalid credentials"
        )
    
    access_token = create_access_token({'sub': user_db.username})


# Websockets endpoints

"""
@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            message: str = await websocket.receive_text()
            for connection in connections:
                await connection.send_text(message)
    except WebSocketDisconnect:
        connections.remove(websocket)
    except Exception as e:
        connections.remove(websocket)
"""


@app.websocket("/ws/chat")
async def ws_chat(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)

    try:
        while True:
            message: str = await websocket.receive_text()
            for connection in connections:
                await connection.send_text(message)
    except WebSocketDisconnect:
        connections.remove(websocket)
    except Exception:  # pragma: no cover
        connections.remove(websocket)


"""
@app.websockets("/ws/game/{game_id}")
async def ws_game(websocket: WebSocket):
    await websocket.accept()
    active_games.setdefault(game_id, []).append(websocket)

    try:
        while True:
            data = await websocket.receive_json()
            for connection in active_games[game_id]:
                await connection.send_json(data)
    except WebSocketDisconnect:
        active_games[game_id].remove(websocket)
"""
