# Базовый образ Python
FROM python:3.12-slim-bookworm

# Рабочая директория внутри контейнера
WORKDIR /app

# Копирование зависимостей проекта
COPY requirements.txt .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всех файлов .py
COPY ./app/*.py .

# Запуск приложения
CMD [ "python", "app.py" ]