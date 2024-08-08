from fastapi import WebSocket, WebSocketDisconnect, Depends
from sqlalchemy.orm import Session
from datetime import datetime

from .connection_manager import connection_manager
from app.models import Message
from app.database import SessionLocal

from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import WebSocket, Depends
from .connection_manager import connection_manager
from app.models import Message
from app.database import get_db

async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
):
    await connection_manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            recipient_id = extract_recipient_id(data)

            if recipient_id:
                await connection_manager.send_message(recipient_id, f"Message from {user_id}: {data}")
            else:
                await connection_manager.broadcast(f"Message from {user_id}: {data}")
                
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id)
        await connection_manager.broadcast(f"User {user_id} left the chat")

def extract_recipient_id(message: str) -> str:
    parts = message.split(":", 1)
    if len(parts) == 2:
        return parts[0].strip()
    return ""
