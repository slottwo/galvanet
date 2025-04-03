from http import HTTPStatus

from fastapi import FastAPI, HTTPException, WebSocket
from fastapi.responses import HTMLResponse

from galvanet.schemas import UserList, UserPublic, UserSchema

# Application
app = FastAPI()

# List to store all connected clients
connections: list[WebSocket] = []


# HTTP endpoints


@app.get("/", response_class=HTMLResponse)
def read_root():
    with open("src/index.html", encoding="utf-8") as file:
        return HTMLResponse(file.read())


@app.get("/users/", response_model=UserList)
def read_users():
    return {"users": ...}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    ...  # create user
    return ...  # created user


@app.get("/users/{user_id}", response_model=UserPublic)
def read_user(user_id: int):
    if ...:  # check user_id
        return ...  # user
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="User not found"
    )


@app.put("/users/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserSchema):
    if ...:  # check user_id
        ...  # update user
        return ...  # updated user
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="User not found"
    )


@app.delete("/users/{user_id}", response_model=UserPublic)
def delete_user(user_id: int, user: UserSchema):
    if ...:  # check user_id
        ...  # delete user
        return ...  # deleted user
    raise HTTPException(
        status_code=HTTPStatus.NOT_FOUND, detail="User not found"
    )


# Websockets endpoints


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
