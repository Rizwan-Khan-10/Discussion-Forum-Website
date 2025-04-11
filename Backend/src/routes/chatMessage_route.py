from fastapi import APIRouter, Depends, Query
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

class EditMessageRequest(BaseModel):
    user_id: str
    message_id: str
    new_message: str

class DeleteMessageRequest(BaseModel):
    user_id: str
    message_id: str

class GetMessagesRequest(BaseModel):
    sender_id: str
    receiver_id: str

@chat_router.post("/get")
async def get_messages_route(request: GetMessagesRequest, db: Session = Depends(get_db)):
    return await get_chat_messages(request.sender_id, request.receiver_id, db)

@chat_router.post("/add")
async def add_message_route(request: ChatMessageRequest, db: Session = Depends(get_db)):
    return await add_chat_message(request, db)

@chat_router.post("/edit")
async def edit_message_route(request: EditMessageRequest, db: Session = Depends(get_db)):
    return await edit_chat_message(request.user_id, request.message_id, request.new_message, db)

@chat_router.post("/delete")
async def delete_message_route(request: DeleteMessageRequest, db: Session = Depends(get_db)):
    return await delete_chat_message(request.user_id, request.message_id, db)
