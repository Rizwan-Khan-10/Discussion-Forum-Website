from fastapi import APIRouter, Depends
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
    return await register_user(request, db)

@login_router.post("/login")
async def login(request: LoginRequest, db: Session = Depends(get_db)):
    return await authenticate_user(request, db)
