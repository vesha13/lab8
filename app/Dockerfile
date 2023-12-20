# Базовый образ Python
FROM python:3.12-slim-bookworm

# Рабочая директория внутри контейнера
WORKDIR /app

# Копирование зависимостей проекта
COPY requirements.txt .
# Копируем остальные файлы в контейнер
COPY app/bot.py .
COPY app/config.py .
COPY app/dbworker.py .
COPY app/database.db .
COPY app/bot.spec .

# Установка зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование всех файлов .py
COPY ./app/*.py .

# Запуск приложения
CMD [ "python", "bot.py" ]