from fastapi import APIRouter, Depends
from sqlmodel import Session
from app.database import get_session
from app.crud import message as crud
from app.schemas import user as schemas
from app import  database

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/", response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, session: Session = Depends(get_session)):
    return crud.create_user(session, user)

@router.get("/", response_model=list[schemas.UserRead])
def get_users(session: Session = Depends(get_session)):
    return crud.get_users(session)
