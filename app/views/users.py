from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import User
from pydantic import BaseModel

user_router = APIRouter()

# Pydantic модель для создания пользователя
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Создание пользователя
@user_router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = User(username=user.username, email=user.email, hashed_password=user.password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Получение списка пользователей
@user_router.get("/users/")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users
