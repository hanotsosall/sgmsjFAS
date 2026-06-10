from typing import Dict
from fastapi import WebSocket

class ChatManager:
    def __init__(self):
        self.active_connections: Dict[int, WebSocket] = {}

    async def connect(self, user_id: int, websocket: WebSocket):
        self.active_connections[user_id] = websocket

    def disconnect(self, user_id: int):
        if user_id in self.active_connections:
            del self.active_connections[user_id]

    async def send_message(self, user_id: int, message: str):
        if user_id in self.active_connections:
            await self.active_connections[user_id].send_text(message)