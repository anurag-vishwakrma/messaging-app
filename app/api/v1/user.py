from fastapi import APIRouter, HTTPException
from fastapi_sqlalchemy import db
from app.schemas.user import UserCreate, UserLogin, Token
from app.models.user import User


from app.utils.jwt import create_token
# from app.crud import user as crud_user

router = APIRouter()

@router.post("/signup")
def signup(user_data: UserCreate):
    # if crud_user.get_user_by_username(db.session, user_data.username):
    #     raise HTTPException(status_code=400, detail="Username already taken")
    # crud_user.create_user(db.session, user_data.username, user_data.password)
    return {"message": "User created"}

# @router.post("/login", response_model=Token)
# def login(user_data: UserLogin):
#     user = crud_user.authenticate_user(db.session, user_data.username, user_data.password)
#     if not user:
#         raise HTTPException(status_code=401, detail="Invalid credentials")
#     token = create_token({"sub": user.username})
#     return {"access_token": token, "token_type": "bearer"}