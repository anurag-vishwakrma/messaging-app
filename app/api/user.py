from fastapi import APIRouter, Depends
from sqlmodel import Session
from .database import get_session
from .crud import message as crud
from .schemas import user as schemas
from . import  database

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    return crud.create_user(session, user)

@router.get("/", response_model=list[schemas.UserRead])
def get_users(session: Session = Depends(get_session)):
    return crud.get_users(session)
