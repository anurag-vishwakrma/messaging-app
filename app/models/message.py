from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ConnectedUser(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    sid: str = Field(max_length=128, nullable=False, unique=True)
    connected_at: datetime = Field(default_factory=datetime.utcnow)

class ChatGroup(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, max_length=120, unique=True)
    created_by: int = Field(foreign_key="user.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

class GroupMember(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    group_id: int = Field(foreign_key="chatgroup.id", nullable=False)
    user_id: int = Field(foreign_key="user.id", nullable=False)
    joined_at: datetime = Field(default_factory=datetime.utcnow)


class Message(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    sender_id: int = Field(foreign_key="user.id", nullable=False)
    receiver_id: Optional[int] = Field(foreign_key="user.id", default=None)
    group_id: Optional[int] = Field(foreign_key="chatgroup.id", default=None)
    content: str = Field(nullable=False, max_length=512)
    sent_at: datetime = Field(default_factory=datetime.utcnow)
    is_read: bool = Field(default=False)
    is_deleted: bool = Field(default=False)





