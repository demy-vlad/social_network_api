from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)

    messages = relationship("Message", back_populates="user")

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))
    chat_id = Column(Integer, ForeignKey('chats.id'))

    user = relationship("User", back_populates="messages")
    chat = relationship("Chat", back_populates="messages")

class Chat(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    messages = relationship("Message", back_populates="chat")