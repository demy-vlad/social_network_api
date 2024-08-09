from fastapi import FastAPI, WebSocket
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.websockets.chat_ws import websocket_endpoint
from app.views.users import user_router
from app.views.chats import chat_router
from app.views.messages import message_router
from app.database import engine, Base

app = FastAPI()

# Mount the static directory to serve files
# app.mount("/static", StaticFiles(directory="static"), name="static")

# app.include_router(user_router)
# app.include_router(chat_router)
app.include_router(message_router)

@app.websocket("/ws/chat/{chat_id}/{user_id}")
async def websocket_endpoint_route(websocket: WebSocket, user_id: str, chat_id:str):
    await websocket_endpoint(websocket, user_id, chat_id)

# Define a route for the root URL
@app.get("/", response_class=FileResponse)
async def read_index():
    return FileResponse('static/index.html')

# Создание таблиц при запуске
Base.metadata.create_all(bind=engine)