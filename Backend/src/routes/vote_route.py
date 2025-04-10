from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from pydantic import BaseModel
from controllers.vote_controller import add_vote_controller, get_vote_controller

vote_router = APIRouter()

class VoteRequest(BaseModel):
    post_id: str
    user_id: str
    vote_type: str

class GetVoteRequest(BaseModel):
    post_id: str
    user_id: str

@vote_router.post("/addVote")
async def add_vote(payload: VoteRequest, db: Session = Depends(get_db)):
    return await add_vote_controller(
        post_id=payload.post_id,
        user_id=payload.user_id,
        vote_type=payload.vote_type,
        db=db
    )

@vote_router.post("/getVote")
async def get_vote(payload: GetVoteRequest, db: Session = Depends(get_db)):
    return await get_vote_controller(
        post_id=payload.post_id,
        user_id=payload.user_id,
        db=db
    )
