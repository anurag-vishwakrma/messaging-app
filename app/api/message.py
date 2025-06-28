from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.crud import message as crud
from app.schemas import message as schemas
from app import database

from fastapi import APIRouter, Depends
from sqlmodel import Session
# from .. import crud, schemas, database

router = APIRouter(prefix="/messages", tags=["Messages"])

@router.post("/", response_model=schemas.MessageRead)
def send_message(message: schemas.MessageCreate, session: Session = Depends(database.get_session)):
    return crud.create_message(session, message)

@router.get("/{user1_id}/{user2_id}", response_model=list[schemas.MessageRead])
def get_conversation(user1_id: int, user2_id: int, session: Session = Depends(database.get_session)):
    return crud.get_messages_between_users(session, user1_id, user2_id)
