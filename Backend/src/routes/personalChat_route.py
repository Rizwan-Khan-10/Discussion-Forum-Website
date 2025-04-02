from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from pydantic import BaseModel
from controllers.personalChat_controller import add_personal_chat, get_personal_chats

personalChat_router = APIRouter()

class PersonalChatRequest(BaseModel):
    user_id: str
    user_list: dict
    last_message: dict | None = None

@personalChat_router.post("/add")
async def add_chat_route(request: PersonalChatRequest, db: Session = Depends(get_db)):
    return await add_personal_chat(request, db)

@personalChat_router.get("/chats")
async def get_chats_route(db: Session = Depends(get_db)):
    return await get_personal_chats(db)
