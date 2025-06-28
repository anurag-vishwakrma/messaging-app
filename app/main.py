from fastapi import FastAPI
from contextlib import asynccontextmanager
from sqlmodel import SQLModel
from database import engine
from api import user, message
import uvicorn
from app.models import User, Message

@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(user.router)
app.include_router(message.router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
