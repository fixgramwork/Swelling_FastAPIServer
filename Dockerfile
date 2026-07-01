FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY pyproject.toml README.md ./
COPY src ./src
COPY services ./services

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -e .

ARG SERVICE_MODULE=services.gateway.app.main:app
ARG PORT=8000

ENV SERVICE_MODULE=${SERVICE_MODULE} \
    PORT=${PORT}

CMD ["sh", "-c", "uvicorn ${SERVICE_MODULE} --host 0.0.0.0 --port ${PORT}"]
