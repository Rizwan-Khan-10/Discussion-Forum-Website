from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from pydantic import BaseModel
from controllers.followedThread_controller import addToFollowThread, getFollowThread

followThread_router = APIRouter()

class FollowThreadRequest(BaseModel):
    post_id: str
    user_id: str

@followThread_router.post("/followThread")
async def save_thread(payload: FollowThreadRequest, db: Session = Depends(get_db)):
    return await addToFollowThread(
        post_id=payload.post_id,
        user_id=payload.user_id,
        db=db
    )

@followThread_router.post("/getFollowThread")
async def get_saved_thread(payload: FollowThreadRequest, db: Session = Depends(get_db)):
    return await getFollowThread(
        post_id=payload.post_id,
        user_id=payload.user_id,
        db=db
    )
