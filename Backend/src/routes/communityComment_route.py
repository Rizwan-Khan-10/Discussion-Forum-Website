from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from controllers.communityComment_controller import (
    add_comment, edit_comment, delete_comment, vote_comment
)
from pydantic import BaseModel

communityComment_router = APIRouter()

class CommentRequest(BaseModel):
    post_id: str
    category_id: str
    user_id: str
    content: str

class VoteRequest(BaseModel):
    post_id: str
    category_id: str
    user_id: str
    vote_type: str  

@communityComment_router.post("/add")
async def add_comment_route(request: CommentRequest, db: Session = Depends(get_db)):
    return await add_comment(request, db)

@communityComment_router.put("/edit")
async def edit_comment_route(post_id: str, category_id: str, content: str, db: Session = Depends(get_db)):
    return await edit_comment(post_id, category_id, content, db)

@communityComment_router.delete("/delete")
async def delete_comment_route(post_id: str, category_id: str, db: Session = Depends(get_db)):
    return await delete_comment(post_id, category_id, db)

@communityComment_router.put("/vote")
async def vote_comment_route(request: VoteRequest, db: Session = Depends(get_db)):
    return await vote_comment(request, db)
