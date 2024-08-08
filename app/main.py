# app/main.py
from fastapi import FastAPI, WebSocket
from app.websockets.chat_ws import websocket_endpoint
from app.views.users import user_router
from app.views.chats import chat_router
from app.database import engine, Base

app = FastAPI()

app.include_router(user_router)
app.include_router(chat_router)

@app.websocket("/ws/chat/{chat_id}/{user_id}")
async def websocket_endpoint_route(websocket: WebSocket, user_id: str):
    await websocket_endpoint(websocket, user_id)

# Создание таблиц при запуске
Base.metadata.create_all(bind=engine)
