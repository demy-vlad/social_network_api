from celery import Celery

celery_app = Celery("tasks", broker="redis://localhost:6379/0")

@celery_app.task
def send_notification(user_id, message):
    # Логика отправки уведомления
    pass