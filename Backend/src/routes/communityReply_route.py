from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from controllers.reply_controller import (
    add_reply, edit_reply, delete_reply, vote_reply
)
from pydantic import BaseModel

communityReply_router = APIRouter()

class replyRequest(BaseModel):
    post_id: str
    category_id: str
    user_id: str
    content: str

class VoteRequest(BaseModel):
    post_id: str
    category_id: str
    user_id: str
    vote_type: str  

@communityReply_router.post("/add")
async def add_reply_route(request: replyRequest, db: Session = Depends(get_db)):
    return await add_reply(request, db)

@communityReply_router.put("/edit")
async def edit_reply_route(post_id: str, category_id: str, content: str, db: Session = Depends(get_db)):
    return await edit_reply(post_id, category_id, content, db)

@communityReply_router.delete("/delete")
async def delete_reply_route(post_id: str, category_id: str, db: Session = Depends(get_db)):
    return await delete_reply(post_id, category_id, db)

@communityReply_router.put("/vote")
async def vote_reply_route(request: VoteRequest, db: Session = Depends(get_db)):
    return await vote_reply(request, db)
