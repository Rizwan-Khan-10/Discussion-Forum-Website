from fastapi import WebSocket
from typing import Dict, List
import asyncio

class WebSocketManager:
    def __init__(self):
        self.rooms: Dict[str, List[WebSocket]] = {}
        self.user_sockets: Dict[str, WebSocket] = {}  

    async def connect(self, code: str, websocket: WebSocket, username: str):
        await websocket.accept()
        
        if code not in self.rooms:
            self.rooms[code] = []
        self.rooms[code].append(websocket)

        self.user_sockets[username] = websocket  

    async def disconnect(self, code: str, websocket: WebSocket, username: str):
        if code in self.rooms:
            self.rooms[code].remove(websocket)
            if not self.rooms[code]:  
                del self.rooms[code]

        if username in self.user_sockets:
            del self.user_sockets[username]

    async def broadcast(self, code: str, message: str):
        if code in self.rooms:
            await asyncio.gather(*[
                ws.send_text(message) for ws in self.rooms[code]
            ])

    async def send_to_user(self, username: str, message: str):
        if username in self.user_sockets:
            await self.user_sockets[username].send_text(message)

websocket_manager = WebSocketManager()
