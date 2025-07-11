from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlmodel import select
from app.database import get_session
from app.models import User
from app.schemas.token import UserLogin, Token
from app.utils.token import verify_password, create_access_token, public

router = APIRouter(prefix="/auth", tags=["Auth"])

@public
@router.post("/login", response_model=Token)
def login(login_data: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == login_data.email)).first()
    if not user or not verify_password(login_data.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(data={"sub": user.email, "user_id":user.id})
    return {"access_token": access_token, "token_type": "bearer"}