# Используем легкий образ Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Сначала копируем зависимости (для кэширования слоев Docker)
COPY requirements.txt .

# Устанавливаем библиотеки
# libpq-dev нужен для сборки psycopg2 (драйвер postgres)
RUN apt-get update && apt-get install -y libpq-dev gcc && \
    pip install --no-cache-dir -r requirements.txt

# Копируем весь код проекта в контейнер
COPY . .

# Указываем переменную окружения, чтобы Python не буферизировал вывод (важно для логов в Docker)
ENV PYTHONUNBUFFERED=1

# Указываем команду запуска
CMD ["python", "app/run.py"]