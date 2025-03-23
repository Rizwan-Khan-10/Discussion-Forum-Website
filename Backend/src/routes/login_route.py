from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from db.connection import get_db
from controllers.login_controller import register_user, authenticate_user
from pydantic import BaseModel

login_router = APIRouter()

class SignupRequest(BaseModel):
    username: str
    email: str
    password: str

class LoginRequest(BaseModel):
    email: str
    password: str

@login_router.post("/register")
async def signup(request: SignupRequest, db: Session = Depends(get_db)):
    user = await register_user(request, db)
    if not user:
        raise HTTPException(status_code=400, detail="User already exists")
    return {"message": "User registered successfully"}

@login_router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    token = await authenticate_user(request, db)
    if not token:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return {"access_token": token, "token_type": "bearer"}
