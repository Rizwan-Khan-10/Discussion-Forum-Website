from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from controllers.user_controller import (
    create_user_profile, get_user_profile, update_user_profile, 
    delete_user_profile, follow_user
)
from pydantic import BaseModel

profile_router = APIRouter()

class UserProfileRequest(BaseModel):
    bio: str = None
    img: str = None
    blockUser: bool = False
    blockCommunity: bool = False
    blockPost: bool = False

@profile_router.post("/createProfile")
async def create_profile(user_id: str, request: UserProfileRequest, db: Session = Depends(get_db)):
    return await create_user_profile(user_id, request, db)

@profile_router.get("/getProfile")
async def get_profile(user_id: str, db: Session = Depends(get_db)):
    return await get_user_profile(user_id, db)

@profile_router.put("/updateProfile")
async def update_profile(user_id: str, request: UserProfileRequest, db: Session = Depends(get_db)):
    return await update_user_profile(user_id, request, db)

@profile_router.delete("/deleteProfile")
async def delete_profile(user_id: str, db: Session = Depends(get_db)):
    return await delete_user_profile(user_id, db)

@profile_router.post("/follow")
async def follow(user_id: str, follow_id: str, db: Session = Depends(get_db)):
    return await follow_user(user_id, follow_id, db)
