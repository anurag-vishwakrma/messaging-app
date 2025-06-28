from sqlmodel import Session, select
from ..models import User, Message
from ..schemas.message import MessageCreate
from ..schemas.user import UserCreate
from app.utils.token import hash_password

# Users
def create_user(session: Session, user: UserCreate):
    hashed_pw = hash_password(user.password)
    user_data = user.dict()
    user_data["password"] = hashed_pw  # Replace plaintext with hashed
    db_user = User(**user_data)
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