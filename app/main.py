from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.websockets.chat_ws import websocket_endpoint
from app.views.users import user_router
from app.views.chats import chat_router
from app.views.messages import message_router
from app.database import engine, Base
import json
from .database import SessionLocal
from app.models import Message
from sqlalchemy.orm import Session
from datetime import datetime

app = FastAPI()

# Mount the static directory to serve files
# app.mount("/static", StaticFiles(directory="static"), name="static")

import logging

logging.basicConfig(level=logging.DEBUG)

# app.include_router(user_router)
# app.include_router(chat_router)
app.include_router(message_router)


connections = []  # This should be a list to keep track of all connected clients

@app.websocket("/ws/chat/{chat_id}/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str, chat_id: str):
    await websocket.accept()
    connections.append(websocket)
    db = SessionLocal()  # Create or get your database session here
    
    try:
        while True:
            data = await websocket.receive_text()
            print(f"Received raw message: {data} from User ID: {user_id}")

            try:
                # Attempt to parse the JSON data
                message_data = json.loads(data)
                print(f"Parsed message data: {message_data}")

                # Save the message to the database
                save_message_to_db(message_data['message'], message_data['userId'], db, chat_id)

                # Broadcast the message to all connected clients
                for connection in connections:
                    if connection != websocket:
                        await connection.send_text(data)
            except json.JSONDecodeError as e:
                print(f"Error decoding JSON: {e}")
    except WebSocketDisconnect:
        print(f"User {user_id} disconnected")
    finally:
        connections.remove(websocket)
        db.close()

def save_message_to_db(message: str, user_id: str, db: Session, chat_id: str):
    db_message = Message(
        message=message,
        timestamp=datetime.utcnow(),
        user_id=user_id,
        chat_id=chat_id
    )
    db.add(db_message)
    db.commit()
    db.refresh(db_message)

# Define a route for the root URL
@app.get("/", response_class=FileResponse)
async def read_index():
    return FileResponse('static/index.html')

# Создание таблиц при запуске
Base.metadata.create_all(bind=engine)