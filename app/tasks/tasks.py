from celery import Celery

app = Celery("tasks", broker="redis://localhost:6379/0")

@app.task
def send_notification(user_id, message):
    # Логика отправки уведомления
    print(f"send_notification user_id [{user_id}]: {message}")
