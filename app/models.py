from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Date, Boolean
from sqlalchemy.orm import relationship
from .database import Base
import uuid

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    birthday = Column(Date)
    gender = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    photo = Column(String)
    hashed_password = Column(String)
    chatting = Column(Boolean, default=False)
    dating = Column(Boolean, default=False)
    gaming = Column(Boolean, default=False)
    vaping = Column(Boolean, default=False)
    single = Column(Boolean, default=False)
    relationships = Column(Boolean, default=False)
    married = Column(Boolean, default=False)
    divorced = Column(Boolean, default=False)
    travel = Column(Boolean, default=False)
    sports = Column(Boolean, default=False)
    music = Column(Boolean, default=False)
    books = Column(Boolean, default=False)
    movies = Column(Boolean, default=False)
    games = Column(Boolean, default=False)
    cook = Column(Boolean, default=False)
    work = Column(Boolean, default=False)
    family = Column(Boolean, default=False)
    animals = Column(Boolean, default=False)

    messages = relationship("Message", back_populates="user")

class Message(Base):
    __tablename__ = "messages"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    message = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(String, ForeignKey('chats.id'))

    user = relationship("User", back_populates="messages")
    chat = relationship("Chat", back_populates="messages")

class Chat(Base):
    __tablename__ = "chats"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, index=True)

    messages = relationship("Message", back_populates="chat")