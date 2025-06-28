from sqlmodel import SQLModel
from datetime import datetime

class MessageCreate(SQLModel):
    sender_id: int
    receiver_id: int
    content: str

class MessageRead(SQLModel):
    id: int
    sender_id: int
    receiver_id: int
    content: str
    timestamp: datetime
