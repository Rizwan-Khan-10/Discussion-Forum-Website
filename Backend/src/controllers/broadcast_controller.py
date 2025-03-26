from fastapi import WebSocket
from typing import Dict

class WebSocketManager:
    def __init__(self):
        self.user_sockets: Dict[str, WebSocket] = {}  

    async def connect(self, websocket: WebSocket, username: str):
        await websocket.accept()
        self.user_sockets[username] = websocket  

    async def disconnect(self, username: str):
        if username in self.user_sockets:
            del self.user_sockets[username]

    async def send_to_user(self, username: str, message: str):
        if username in self.user_sockets:
            await self.user_sockets[username].send_text(message)

websocket_manager = WebSocketManager()
