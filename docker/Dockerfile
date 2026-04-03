# ---- Base ----
FROM python:3.10-slim

# Prevent python buffering
ENV PYTHONUNBUFFERED=1

# System deps (FAISS needs this)
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working dir
WORKDIR /app

# Copy requirements first (cache optimization)
COPY backend/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy backend + frontend
COPY backend /app/backend
COPY frontend /app/frontend

# 🔥 Create data dirs (important)
RUN mkdir -p /app/backend/data/faiss \
    && mkdir -p /app/backend/data/metadata \
    && mkdir -p /app/backend/data/raw_docs \
    && mkdir -p /app/backend/data/processed

# Expose port
EXPOSE 8000

# Start app
CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]