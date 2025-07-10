FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем утилиты мониторинга
RUN apt-get update && apt-get install -y --no-install-recommends \
    iotop htop procps && rm -rf /var/lib/apt/lists/*

COPY src .

RUN chgrp -R 0 /app && chmod -R g=u /app

EXPOSE 8000

# Запуск Uvicorn через gunicorn для лучшей стабильности
CMD ["gunicorn", "app.main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]