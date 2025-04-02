from http import HTTPStatus

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from galvanet.schemas import UserDB, UserList, UserPublic, UserSchema

# Application
app = FastAPI()

# List to store all connected clients
connections: list[WebSocket] = []

# Provisory database
database = []


# Root endpoint
@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("src/index.html", encoding="utf-8") as file:
        return HTMLResponse(file.read())


# Users endpoints
@app.get("/users/", response_model=UserList)
def read_users():
    return {"users": database}


@app.get("/users/{user_id}", response_model=UserPublic)
def read_user(user_id: int):
    for user in database:
        if user.id == user_id:
            return user
    return HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='user not found')


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_w_id = UserDB(id=1 + len(database), **user.model_dump())
    database.append(user_w_id)
    return user_w_id


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    user_w_id = UserDB(id=user_id, **user.model_dump())
    for k, v in enumerate(database):
        if v.id == user_id:
            database[k] = user_w_id
            return user_w_id


# WebSocket endpoint
@app.websocket("/ws")
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            message: str = await websocket.receive_text()
            for connection in connections:
                await connection.send_text(f"User says: {message}")
    except Exception as e:
        connections.remove(websocket)
        print("Conexão encerrada:", e)
