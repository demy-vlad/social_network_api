from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.websockets.chat_ws import websocket_endpoint
from app.views.users import user_router
from app.views.chats import chat_router
from app.views.messages import message_router
from app.database import engine, Base
import json

app = FastAPI()

# Mount the static directory to serve files
# app.mount("/static", StaticFiles(directory="static"), name="static")

import logging

logging.basicConfig(level=logging.DEBUG)

# app.include_router(user_router)
# app.include_router(chat_router)
app.include_router(message_router)

@app.websocket("/ws/chat/{chat_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, chat_id: str, user_id: str):
    await websocket.accept()
    logging.info(f"User {user_id} connected to chat {chat_id}")
    try:
        while True:
            data = await websocket.receive_text()
            logging.info(f"Received message: {data} from User ID: {user_id}")
            # Отправка сообщения всем клиентам
            await websocket.send_text(f"Message from {user_id}: {data}")
    except WebSocketDisconnect as e:
        logging.error(f"WebSocket disconnected: {e}")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")

# Define a route for the root URL
@app.get("/", response_class=FileResponse)
async def read_index():
    return FileResponse('static/index.html')

# Создание таблиц при запуске
Base.metadata.create_all(bind=engine)