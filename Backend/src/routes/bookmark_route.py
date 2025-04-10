from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from pydantic import BaseModel
from controllers.bookmark_controller import addToBookmark, getBookmark

bookmark_router = APIRouter()

class BookmarkRequest(BaseModel):
    post_id: str
    user_id: str

@bookmark_router.post("/addBookmark")
async def save_thread(payload: BookmarkRequest, db: Session = Depends(get_db)):
    return await addToBookmark(
        post_id=payload.post_id,
        user_id=payload.user_id,
        db=db
    )

@bookmark_router.post("/getBookmark")
async def get_saved_thread(payload: BookmarkRequest, db: Session = Depends(get_db)):
    return await getBookmark(
        post_id=payload.post_id,
        user_id=payload.user_id,
        db=db
    )
