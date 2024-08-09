// websocket.js

// Создаем новое WebSocket соединение
const ws = new WebSocket("ws://localhost:8000/ws/chat/2");

// Обработка события открытия соединения
ws.onopen = () => {
    console.log("WebSocket соединение установлено.");
    // Отправляем сообщение серверу
    ws.send("Hello, Chat 1!");
};

// Обработка входящих сообщений от сервера
ws.onmessage = (event) => {
    console.log("Сообщение от сервера: ", event.data);
};

// Обработка ошибок WebSocket
ws.onerror = (error) => {
    console.error("Ошибка WebSocket: ", error);
};

// Обработка закрытия соединения
ws.onclose = () => {
    console.log("WebSocket соединение закрыто.");
};
