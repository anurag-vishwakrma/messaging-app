from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str = Field(nullable=False, max_length=80)
    last_name: Optional[str] = Field(default=None, max_length=80)
    display_name: Optional[str] = Field(default=None, max_length=180)
    email: str = Field(nullable=False, unique=True, max_length=120)
    phone: Optional[str] = Field(default=None, unique=True, max_length=13)
    password: str = Field(nullable=False, max_length=128)
    is_super_user: bool = Field(default=False)
    is_active: bool = Field(default=True)
    created_date: Optional[datetime] = Field(default_factory=datetime.utcnow)
