# Официальный облегчённый образ Python.
FROM python:3.12-slim

# Не создавать файлы .pyc и сразу выводить журналы приложения в Docker.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Все следующие команды выполняются внутри каталога /app.
WORKDIR /app

# Сначала копируем только зависимости — так Docker сможет кэшировать их установку.
COPY requirements.txt .
RUN python -m pip install --no-cache-dir -r requirements.txt

# Копируем исходный код и создаём каталог для постоянной базы данных.
COPY . .
RUN mkdir -p /app/data

# Приложение внутри контейнера принимает запросы на порту 8000.
EXPOSE 8000

# Команда запуска по умолчанию. В compose.yaml она будет дополнена миграциями.
CMD ["gunicorn", "learning_log.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "4", "--timeout", "60"]
