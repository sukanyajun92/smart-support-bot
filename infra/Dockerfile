# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY services/user_service/ user_service/
COPY tests/ tests/
COPY infra/.env .

EXPOSE 8000

CMD ["uvicorn", "user_service.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
