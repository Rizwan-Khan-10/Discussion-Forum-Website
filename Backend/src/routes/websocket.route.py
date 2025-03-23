from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Path
import json
from controllers.broadcast_controller import websocket_manager

router = APIRouter()

@router.websocket("/ws/{userId}")
async def websocket_endpoint(
    websocket: WebSocket,
    code: str,
    username: str = Path(..., title="Username")
):
    username = username.replace("%20", " ") 
    await websocket_manager.connect(code, websocket, username)  

    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        await websocket_manager.disconnect(code, websocket, username)  
