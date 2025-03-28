from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from controllers.follow_controller import follow_user, unfollow_user
from pydantic import BaseModel

follow_router = APIRouter()

class FollowRequest(BaseModel):
    user_id: str
    follow_id: str

@follow_router.post("/follow")
async def follow(request: FollowRequest, db: Session = Depends(get_db)):
    return await follow_user(request, db)

@follow_router.post("/unfollow")
async def unfollow(request: FollowRequest, db: Session = Depends(get_db)):
    return await unfollow_user(request, db)
