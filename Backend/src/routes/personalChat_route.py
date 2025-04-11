from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from controllers.personalChat_controller import get_personal_chats

personalChat_router = APIRouter()

@personalChat_router.get("/chats")
async def get_chats_route(user_id: str, db: Session = Depends(get_db)):
    return await get_personal_chats(user_id, db)
