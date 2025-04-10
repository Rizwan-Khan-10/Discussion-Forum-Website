from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from controllers.reply_controller import (
    add_reply, get_replies, edit_reply, delete_reply
)
from pydantic import BaseModel

reply_router = APIRouter()

class ReplyRequest(BaseModel):
    comment_id: str
    user_id: str
    content: str

class EditReplyRequest(BaseModel):
    comment_id: str
    user_id: str
    reply_id: str
    new_content: str

class GetReplyRequest(BaseModel):
    comment_id: str 

class DeleteReplyRequest(BaseModel):
    comment_id: str
    reply_id:str

@reply_router.post("/addReply")
async def add_reply_route(request: ReplyRequest, db: Session = Depends(get_db)):
    return await add_reply(request, db)

@reply_router.post("/editReply")
async def edit_reply_route(request: EditReplyRequest, db: Session = Depends(get_db)):
    return await edit_reply(request.user_id, request.comment_id, request.reply_id, request.new_content, db)

@reply_router.post("/deleteReply")
async def delete_reply_route(request: DeleteReplyRequest, db: Session = Depends(get_db)):
    return await delete_reply(request.comment_id, request.reply_id, db)

@reply_router.post("/getReplies")
async def get_reply_route(request: GetReplyRequest, db: Session = Depends(get_db)):
    return await get_replies(request.comment_id, db)
