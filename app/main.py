from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.database import engine
from app.api import user, message ,auth
from fastapi.staticfiles import StaticFiles
from app.models import User, Message  # ensures models are loaded for Alembic
import uvicorn
import os
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(
    title="Messaging App API",
    description="A backend service built with FastAPI, SQLModel, Alembic, and PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

@app.get("/", response_class=HTMLResponse)
def root():
    with open(f"{STATIC_DIR}/intro.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# Register API routers
app.include_router(user.router)
app.include_router(message.router)
app.include_router(auth.router)

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
