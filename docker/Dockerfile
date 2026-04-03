FROM python:3.10

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/app

WORKDIR /app

# ---- Install lightweight deps first (FAST layer) ----
COPY backend/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# ---- Install heavy deps separately (cached layer) ----
COPY backend/requirements-heavy.txt .
RUN pip install -r requirements-heavy.txt

# ---- Copy code (won't break cache unless code changes) ----
COPY backend /app/backend
COPY frontend /app/frontend

# ---- Create data dirs ----
RUN mkdir -p /app/backend/data/faiss \
    && mkdir -p /app/backend/data/metadata \
    && mkdir -p /app/backend/data/raw_docs \
    && mkdir -p /app/backend/data/processed

EXPOSE 8000

CMD ["uvicorn", "backend.app.main:app", "--host", "0.0.0.0", "--port", "8000"]