from fastapi import FastAPI, WebSocket
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
async def websocket_endpoint(websocket: WebSocket, user_id: str, chat_id: str):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        logging.debug(f"Data received: {data}")
        try:
            message_data = json.loads(data)
            message = message_data.get('message')
            user_id = message_data.get('userId')
            
            logging.debug(f"Message: {message}, User ID: {user_id}")
            
            await websocket.send_text(json.dumps({
                'message': message,
                'userId': user_id
            }))
        except json.JSONDecodeError:
            logging.error("Error decoding JSON")

# Define a route for the root URL
@app.get("/", response_class=FileResponse)
async def read_index():
    return FileResponse('static/index.html')

# Создание таблиц при запуске
Base.metadata.create_all(bind=engine)