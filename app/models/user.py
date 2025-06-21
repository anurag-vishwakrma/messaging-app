from sqlalchemy import Column, Integer, String, func, Boolean,DateTime
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    name = Column(String, unique=True, index=True)
    is_super_user = Column(Boolean, default=False)
    hashed_password = Column(String)

    create_date = Column(DateTime, server_default=func.now())
    create_uid = Column(Integer)
    write_date = Column(DateTime, onupdate=func.now(), server_default=func.now())
    write_uid = Column(Integer)