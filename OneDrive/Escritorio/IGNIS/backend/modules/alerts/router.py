"""WebSocket endpoint and broadcast for real-time alerts."""
import json
from fastapi import APIRouter, WebSocket, WebSocketDisconnect

router = APIRouter(tags=["alerts"])

# Active WebSocket connections
connections: list[WebSocket] = []


async def broadcast_alert(message: dict):
    """Send alert JSON to all connected clients."""
    payload = json.dumps(message)
    dead = []
    for ws in connections:
        try:
            await ws.send_text(payload)
        except Exception:
            dead.append(ws)
    for ws in dead:
        try:
            connections.remove(ws)
        except ValueError:
            pass


@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Optional: handle ping/pong or commands; for demo we only push from server
    except WebSocketDisconnect:
        pass
    finally:
        try:
            connections.remove(websocket)
        except ValueError:
            pass
