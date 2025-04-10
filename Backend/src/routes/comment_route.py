from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from controllers.comment_controller import (
    add_comment, get_comments, delete_comment, edit_comment
)
from pydantic import BaseModel

comment_router = APIRouter()

class CommentRequest(BaseModel):
    post_id: str
    user_id: str
    content: str

class EditCommentRequest(BaseModel):
    post_id: str
    user_id: str
    comment_id: str
    new_content: str

class VoteRequest(BaseModel):
    comment_id: str
    user_id: str
    vote_type: str 

class GetCommentRequest(BaseModel):
    post_id: str 

class DeleteCommentRequest(BaseModel):
    post_id: str
    comment_id:str

@comment_router.post("/add")
async def add_comment_route(request: CommentRequest, db: Session = Depends(get_db)):
    return await add_comment(request, db)

@comment_router.post("/edit")
async def edit_comment_route(request: EditCommentRequest, db: Session = Depends(get_db)):
    return await edit_comment(request.user_id, request.post_id, request.comment_id, request.new_content, db)

@comment_router.post("/delete")
async def delete_comment_route(request: DeleteCommentRequest, db: Session = Depends(get_db)):
    return await delete_comment(request.post_id, request.comment_id, db)

@comment_router.post("/get")
async def get_comment_route(request: GetCommentRequest, db: Session = Depends(get_db)):
    return await get_comments(request.post_id, db)
