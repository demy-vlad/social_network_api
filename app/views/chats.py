from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import Chat
from pydantic import BaseModel

chat_router = APIRouter()

# Pydantic модель для создания чата
class ChatCreate(BaseModel):
    name: str

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создание чата
@chat_router.post("/chats/")
def create_chat(chat: ChatCreate, db: Session = Depends(get_db)):
    db_chat = Chat(name=chat.name)
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

# Получение списка чатов
@chat_router.get("/chats/")
def read_chats(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    chats = db.query(Chat).offset(skip).limit(limit).all()
    return chats
