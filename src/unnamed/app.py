from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
import uvicorn

app = FastAPI()

connections: list[WebSocket] = []


@app.get('/')
async def root():
    with open("src/index.html") as file:
        return HTMLResponse(file.read())


@app.websocket('/ws')
async def ws_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            msg = await websocket.receive_text()
            for connection in connections:
                await connection.send_text(f"User {websocket.client.host} says: {msg}")
    except Exception as e:
        connections.remove(websocket)
        print("Conexção encerrada:", e)
