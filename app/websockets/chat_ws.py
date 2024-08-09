from fastapi import WebSocket, WebSocketDisconnect
from sqlalchemy.orm import Session
from datetime import datetime

from .connection_manager import connection_manager
from app.models import Message
from app.database import SessionLocal


async def websocket_endpoint(
    websocket: WebSocket,
    user_id: str,
    chat_id: str,
):
    # Создание сессии базы данных вручную
    db = SessionLocal()
    await connection_manager.connect(user_id, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            recipient_id = extract_recipient_id(data)

            if recipient_id:
                await connection_manager.send_message(recipient_id, f"{user_id}: {data}")
            else:
                update_messages(data, user_id, db, chat_id)  # Передаем db в функцию update_messages
                await connection_manager.broadcast(f"{user_id}: {data}")
                
    except WebSocketDisconnect:
        connection_manager.disconnect(user_id)
        await connection_manager.broadcast(f"User {user_id} left the chat")
    finally:
        db.close()  # Закрываем сессию базы данных

def extract_recipient_id(message: str) -> str:
    parts = message.split(":", 1)
    if len(parts) == 2:
        return parts[0].strip()
    return ""

def update_messages(data: str, user_id: str, db: Session, chat_id: str):
    db_message = Message(
            message=data,
            timestamp=datetime.utcnow(),
            user_id=user_id,
            chat_id=chat_id
        )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)