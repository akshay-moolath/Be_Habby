from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from ..db import engine
from ..models import User
from ..schemas import UserCreate, Token
from ..auth_utils import get_password_hash, verify_password, create_access_token


router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register")
def register(user_in: UserCreate):
    with Session(engine) as session:
        statement = select(User).where(User.username == user_in.username)
        existing = session.exec(statement).first()
        if existing:
            raise HTTPException(status_code=400, detail="Username already registered")
        user = User(username=user_in.username, hashed_password=get_password_hash(user_in.password))
        session.add(user)
        session.commit()
        session.refresh(user)
        return {"id": user.id, "username": user.username}


@router.post("/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        statement = select(User).where(User.username == form_data.username)
        user = session.exec(statement).first()
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Incorrect username or password")
        access_token = create_access_token({"sub": str(user.id), "username": user.username})
        return {"access_token": access_token, "token_type": "bearer"}