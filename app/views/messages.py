from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Message
from typing import Optional

message_router = APIRouter()

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Получение списка сообщений
@message_router.get("/messages/")
def read_messages(
    skip: int = 0,
    limit: int = 10,
    chat_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Message)
    
    if chat_id is not None:
        query = query.filter(Message.chat_id == chat_id)
    
    messages = query.offset(skip).limit(limit).all()
    return messages