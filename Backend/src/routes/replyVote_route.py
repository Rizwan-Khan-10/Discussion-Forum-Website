from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from pydantic import BaseModel
from controllers.replyVote_controller import add_vote_controller, get_vote_controller

replyVote_router = APIRouter()

class VoteRequest(BaseModel):
    reply_id: str
    user_id: str
    vote_type: str

class GetVoteRequest(BaseModel):
    reply_id: str
    user_id: str

@replyVote_router.post("/addReplyVote")
async def add_vote(payload: VoteRequest, db: Session = Depends(get_db)):
    return await add_vote_controller(
        reply_id=payload.reply_id,
        user_id=payload.user_id,
        vote_type=payload.vote_type,
        db=db
    )

@replyVote_router.post("/getReplyVote")
async def get_vote(payload: GetVoteRequest, db: Session = Depends(get_db)):
    return await get_vote_controller(
        reply_id=payload.reply_id,
        user_id=payload.user_id,
        db=db
    )
