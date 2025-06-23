# messaging_app/app/main.py
from fastapi import FastAPI
from app.api.v1 import user
from fastapi_sqlalchemy import DBSessionMiddleware
import os

app = FastAPI(title="Messaging App")

# Add FastAPI-SQLAlchemy middleware
app.add_middleware(
    DBSessionMiddleware,
    db_url=os.getenv("DATABASE_URL", "postgresql+psycopg2://anurag:anurag@localhost:5432/anurag")
)

app.include_router(user.router, prefix="/api/v1/auth", tags=["Auth"])
