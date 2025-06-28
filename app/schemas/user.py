from sqlmodel import SQLModel
from typing import Optional
from datetime import datetime


class UserBase(SQLModel):
    first_name: str
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    email: str
    phone: Optional[str] = None
    is_super_user: bool = False
    is_active: bool = True


class UserCreate(UserBase):
    password: str


class UserRead(UserBase):
    id: int
    created_date: Optional[datetime]


class UserUpdate(SQLModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    display_name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    password: Optional[str] = None
    is_super_user: Optional[bool] = None
    is_active: Optional[bool] = None