import socketio
from socketio import ASGIApp
from app.sockets.events import register_socketio_events
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from app.database import engine
from app.api import user, message ,auth
from fastapi.staticfiles import StaticFiles
from app.models import User, Message  # ensures models are loaded for Alembic
from app.utils.token import verify_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware


security = HTTPBearer()
import uvicorn
import os
from app.utils.token import public

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")

app = FastAPI(
    title="Messaging App API",
    description="A backend service built with FastAPI, SQLModel, Alembic, and PostgreSQL.",
    version="1.0.0",
    lifespan=lifespan,
    dependencies=[Depends(verify_token)]
)
# Register Socket.IO events
register_socketio_events(sio)



app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/protected")
def protected_route(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    return {"message": "Token received", "token": token}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

@public
@app.get("/", response_class=HTMLResponse, include_in_schema=False)
def root():
    with open(f"{STATIC_DIR}/intro.html", "r", encoding="utf-8") as f:
        return HTMLResponse(content=f.read())

# Register API routers
app.include_router(user.router)
app.include_router(message.router)
app.include_router(auth.router)

# Mount ASGI app
asgi_app = ASGIApp(sio, other_asgi_app=app)

if __name__ == "__main__":
    uvicorn.run("app.main:asgi_app", host="0.0.0.0", port=8000, reload=True)
