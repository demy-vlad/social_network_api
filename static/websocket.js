const emojiBlocks = document.querySelectorAll('.emoji-block');
const messageInput = document.getElementById('message-input');

// Добавляем функциональность выбора эмодзи
emojiBlocks.forEach(block => {
    block.addEventListener('click', () => {
        messageInput.value += block.textContent;
    });
});

const chatId = "chat1"; // ID чата
const userIdInput = document.getElementById('user-id-input');
const sendButton = document.getElementById('send-button');
const messageList = document.getElementById('message-list');
const popup = document.getElementById('popup');
const overlay = document.getElementById('overlay');
const okButton = document.getElementById('ok-button');
let ws;

function connectWebSocket() {
    const userId = userIdInput.value;
    if (userId) {
        if (ws) {
            ws.close();
        }
        // Определение протокола для WebSocket
        const protocol = location.protocol === 'https:' ? 'wss:' : 'ws:';
        ws = new WebSocket(`${protocol}//${location.host}/ws/chat/${chatId}/${userId}`);
        ws.onopen = () => {
            console.log("WebSocket connection established.");
        };
        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                const message = data.message;
                const sender = data.userId;
        
                console.log("Message received:", message); // Debugging message reception
        
                // Отображаем входящие сообщения
                const messageElement = document.createElement('div');
                messageElement.className = 'message';
                messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
                messageList.appendChild(messageElement);
                messageList.scrollTop = messageList.scrollHeight; // Scroll to the bottom
            } catch (e) {
                console.error("Error parsing message data:", e);
            }
        };
        ws.onerror = (error) => {
            console.error("WebSocket error: ", error);
        };
        ws.onclose = () => {
            console.log("WebSocket connection closed.");
        };
    } else {
        alert("Please enter your user name!");
    }
}

function displayMessage(message, sender) {
    const messageElement = document.createElement('div');
    messageElement.className = 'message';
    messageElement.innerHTML = `<strong>${sender}:</strong> ${message}`;
    messageList.appendChild(messageElement);
    messageList.scrollTop = messageList.scrollHeight; // Scroll to the bottom
}

sendButton.addEventListener('click', () => {
    const userId = userIdInput.value;
    if (ws && messageInput.value) {
        if (ws.readyState === WebSocket.OPEN) { // Check if WebSocket is open
            console.log("Sending message:", messageInput.value); // Debugging message sending
            
            // Отображаем отправленное сообщение немедленно
            displayMessage(messageInput.value, userId);
            
            const messageData = {
                message: messageInput.value,
                userId: userId
            };
            ws.send(JSON.stringify(messageData));
            messageInput.value = '';
        } else {
            console.warn("WebSocket is not open. Cannot send message.");
        }
    }
});

messageInput.addEventListener('keypress', (event) => {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendButton.click();
    }
});

userIdInput.addEventListener('blur', connectWebSocket);

// Display the popup when the page loads
window.addEventListener('load', () => {
    popup.style.display = 'block';
    overlay.style.display = 'block';
});

// Close the popup when the OK button is clicked
okButton.addEventListener('click', () => {
    popup.style.display = 'none';
    overlay.style.display = 'none';
});