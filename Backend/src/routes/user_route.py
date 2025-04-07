from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from controllers.user_controller import (
    get_user_profile, update_user_profile, 
    delete_user_profile
)
from typing import Optional
from fastapi import UploadFile, File, Form, Header
from pydantic import BaseModel

profile_router = APIRouter()

class UserProfileRequest(BaseModel):
    bio: str = None
    img: str = None
    blockUser: bool = False
    blockCommunity: bool = False
    blockPost: bool = False

@profile_router.get("/get")
async def get_profile(user_id: str = Header(...), db: Session = Depends(get_db)):
    return await get_user_profile(user_id, db)

@profile_router.post("/update")
async def update_profile(
    user_id: str = Header(...),
    username: str = Form(...),
    bio: Optional[str] = Form(None),
    profilePic: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db)
):
    return await update_user_profile(user_id, username, bio, profilePic, db)

@profile_router.delete("/delete")
async def delete_profile(user_id: str, db: Session = Depends(get_db)):
    return await delete_user_profile(user_id, db)