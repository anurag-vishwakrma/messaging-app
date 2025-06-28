from sqlmodel import Session, select
from ..models import User, Message
from ..schemas.message import MessageCreate
from ..schemas.user import UserCreate

# Users
def create_user(session: Session, user: UserCreate):
    db_user = User(**user.dict())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_users(session: Session):
    return session.exec(select(User)).all()

# Messages
def create_message(session: Session, message: MessageCreate):
    db_msg = Message(**message.dict())
    session.add(db_msg)
    session.commit()
    session.refresh(db_msg)
    return db_msg

def get_messages_between_users(session: Session, user1_id: int, user2_id: int):
    return session.exec(
        select(Message).where(
            ((Message.sender_id == user1_id) & (Message.receiver_id == user2_id)) |
            ((Message.sender_id == user2_id) & (Message.receiver_id == user1_id))
        )
    ).all()