from http import HTTPStatus

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

from galvanet.schemas import UserDB, UserPublic, UserSchema

# Application
app = FastAPI()

# List to store all connected clients
connections: list[WebSocket] = []

# Provisory database
database = []


# Root endpoint
@app.get("/", status_code=HTTPStatus.OK, response_class=HTMLResponse)
async def read_root():
    with open("src/index.html", encoding="utf-8") as file:
        return HTMLResponse(file.read())


# Users endpoint
@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
async def create_user(user: UserSchema):
    user_w_id = UserDB(id=1 + len(database), **user.model_dump())
    database.append(user_w_id)
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
