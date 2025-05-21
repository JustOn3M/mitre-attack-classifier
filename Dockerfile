# Используем официальный Python-образ
FROM python:3.11-slim

# Установка зависимостей системы
RUN apt-get update && apt-get install -y \
    git \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Установка torch CPU-only перед остальными зависимостями
RUN pip install --no-cache-dir torch==2.2.2+cpu --index-url https://download.pytorch.org/whl/cpu

# Копирование приложения
WORKDIR /app
COPY . .

# Установка остальных Python-зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Проброс порта Streamlit (по умолчанию 8501)
EXPOSE 8501

# Запуск приложения
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]