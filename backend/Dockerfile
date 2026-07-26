# Backend image: FastAPI served by uvicorn.
FROM python:3.12-slim

# Keep Python output unbuffered so logs stream promptly in Docker.
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Install dependencies first to leverage Docker layer caching.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source.
COPY app ./app

EXPOSE 8000

# Bind to 0.0.0.0 so the container is reachable from other services/hosts.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
