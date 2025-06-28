from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime

# User
class UserCreate(SQLModel):
    username: str
    email: str

class UserRead(SQLModel):
    id: int
    username: str
    email: str