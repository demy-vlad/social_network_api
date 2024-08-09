# Базовый образ Python
FROM python:3.11-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы приложения в контейнер
COPY . .

# Экспонируем порт
EXPOSE 5000

# Команда для запуска Flask-приложения
CMD ["flask", "run", "--host=0.0.0.0"]