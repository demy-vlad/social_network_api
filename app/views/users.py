from datetime import date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models import User
from pydantic import BaseModel

user_router = APIRouter()

# Pydantic модель для создания пользователя
class UserCreate(BaseModel):
    username: str
    birthday: date
    gender: str
    photo: str
    email: str
    hashed_password: str
    chatting: bool
    dating: bool
    gaming: bool
    vaping: bool
    single: bool
    relationships: bool
    married: bool
    divorced: bool
    travel: bool
    sports: bool
    music: bool
    books: bool
    movies: bool
    games: bool
    cook: bool
    work: bool
    family: bool
    animals: bool

# Зависимость для получения сессии базы данных
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@user_router.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # Проверьте, существует ли уже пользователь с таким email
    existing_user = db.query(User).filter(User.email == user.email).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with email {user.email} already exists."
        )
    
    # Создайте нового пользователя
    db_user = User(
        username=user.username,
        birthday=user.birthday,
        gender=user.gender,
        photo=user.photo,
        email=user.email,
        hashed_password=user.hashed_password,
        chatting = user.chatting,
        dating = user.dating,
        gaming = user.gaming,
        vaping = user.vaping,
        single = user.single,
        relationships = user.relationships,
        married = user.married,
        divorced = user.divorced,
        travel = user.travel,
        sports = user.sports,
        music = user.music,
        books = user.books,
        movies = user.movies,
        games = user.games,
        cook = user.cook,
        work = user.work,
        family = user.family,
        animals = user.animals,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Получение списка пользователей
@user_router.get("/users/")
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    users = db.query(User).offset(skip).limit(limit).all()
    return users