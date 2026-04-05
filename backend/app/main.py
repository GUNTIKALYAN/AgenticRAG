import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from app.core.startup import lifespan
from app.api.routes import query, ingest, health

app = FastAPI(lifespan=lifespan)

app.include_router(query.router, prefix="/api")
app.include_router(ingest.router, prefix="/api")
app.include_router(health.router, prefix="/api")

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")

print("FRONTEND_DIR:", FRONTEND_DIR)
print("CSS Exists:", os.path.exists(os.path.join(FRONTEND_DIR, "css", "style.css")))

app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

@app.get("/")
def home():
    return FileResponse(os.path.join(FRONTEND_DIR, "index.html"))

@app.get("/chat")
def chat():
    return FileResponse(os.path.join(FRONTEND_DIR, "chat.html"))