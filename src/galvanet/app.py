from http import HTTPStatus

from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

# Application
app = FastAPI()

# List to store all connected clients
connections: list[WebSocket] = []


# Root endpoint
@app.get('/', status_code=HTTPStatus.OK)
async def root():
    with open("src/index.html", encoding='utf-8') as file:
        return HTMLResponse(file.read())


# WebSocket endpoint
@app.websocket('/ws')
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
