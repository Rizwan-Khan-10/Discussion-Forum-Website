from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from pydantic import BaseModel
from controllers.chatMessage_controller import (
    add_chat_message, edit_chat_message, delete_chat_message, get_chat_messages
)

chat_router = APIRouter()

class ChatMessageRequest(BaseModel):
    receiver_id: str
    sender_id: str
    message: str
    time: str 

@chat_router.get("/messages")
async def get_messages_route(db: Session = Depends(get_db)):
    return await get_chat_messages(db)

@chat_router.post("/add")
async def add_message_route(request: ChatMessageRequest, db: Session = Depends(get_db)):
    return await add_chat_message(request, db)

@chat_router.put("/edit")
async def edit_message_route(message_id: str, message: str, db: Session = Depends(get_db)):
    return await edit_chat_message(message_id, message, db)

@chat_router.delete("/delete")
async def delete_message_route(message_id: str, db: Session = Depends(get_db)):
    return await delete_chat_message(message_id, db)