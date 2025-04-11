from sqlalchemy.orm import Session
from models.chatMessage import ChatMessage
from models.user import User
from models.personalChat import PersonalChat
from models.userProfile import UserProfile
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware
from pydantic import BaseModel
from datetime import datetime
import json

class ChatMessageRequest(BaseModel):
    receiver_id: str
    sender_id: str
    message: str
    time: str  

async def add_chat_message(request: ChatMessageRequest, db: Session):
    try:
        sender = db.query(User).filter(User.user_id == request.sender_id).first()
        receiver = db.query(User).filter(User.user_id == request.receiver_id).first()

        if not sender or not receiver:
            raise APIError(status_code=404, detail="Sender or receiver not found.")

        encrypted_message_obj = EncryptionMiddleware.encrypt({"message": request.message})
        encrypted_message = encrypted_message_obj["message"]

        new_message = ChatMessage(
            receiver_id=request.receiver_id,
            sender_id=request.sender_id,
            message=encrypted_message,
            time=request.time  # Don't call .isoformat() here
        )
        db.add(new_message)

        participants = sorted([request.sender_id, request.receiver_id])
        personal_chat = db.query(PersonalChat).filter(
            PersonalChat.user_list.contains(participants)
        ).first()

        encrypted_last_msg = EncryptionMiddleware.encrypt({
            "message": request.message,
            "time": request.time  # Store it as-is, no .isoformat()
        })

        if personal_chat:
            personal_chat.last_message = encrypted_last_msg
        else:
            new_chat = PersonalChat(
                user_id=request.sender_id,
                user_list=participants,
                last_message=encrypted_last_msg
            )
            db.add(new_chat)

        db.commit()
        db.refresh(new_message)

        return APIResponse.success(data={
            "message_id": new_message.message_id,
            "receiver_id": new_message.receiver_id,
            "sender_id": new_message.sender_id,
            "message": request.message,
            "time": str(new_message.time)  # Safe for response
        }, message="Chat message added successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def edit_chat_message(user_id: str, message_id: str, new_message: str, db: Session):
    try:
        chat_message = db.query(ChatMessage).filter(ChatMessage.message_id == message_id).first()
        if not chat_message:
            raise APIError(status_code=404, detail="Chat message not found.")

        if chat_message.sender_id != user_id:
            raise APIError(status_code=403, detail="User not authorized to edit this message.")

        encrypted = EncryptionMiddleware.encrypt({"message": new_message})
        chat_message.message = encrypted["message"]

        participants = sorted([chat_message.sender_id, chat_message.receiver_id])
        personal_chat = db.query(PersonalChat).filter(
            PersonalChat.user_list.contains(participants)
        ).first()

        if personal_chat:
            encrypted_last_msg = EncryptionMiddleware.encrypt({
                "message": new_message,
                "time": str(chat_message.time)  # Ensure this is safe
            })
            personal_chat.last_message = encrypted_last_msg

        db.commit()
        db.refresh(chat_message)

        return APIResponse.success(data={
            "message_id": chat_message.message_id,
            "receiver_id": chat_message.receiver_id,
            "sender_id": chat_message.sender_id,
            "message": new_message,
            "time": str(chat_message.time)
        }, message="Chat message edited successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def get_chat_messages(sender_id: str, receiver_id: str, db: Session):
    try:
        messages = db.query(ChatMessage).filter(
            ((ChatMessage.sender_id == sender_id) & (ChatMessage.receiver_id == receiver_id)) |
            ((ChatMessage.sender_id == receiver_id) & (ChatMessage.receiver_id == sender_id))
        ).order_by(ChatMessage.time.asc()).all()

        if not messages:
            return APIResponse.success(data=[], message="No chat messages found.")

        decrypted_messages = []
        for message in messages:
            decrypted_text = DecryptionMiddleware.decrypt({"message": message.message})["message"]

            decrypted_messages.append({
                "message_id": message.message_id,
                "sender_id": message.sender_id,
                "receiver_id": message.receiver_id,
                "message": decrypted_text,
                "time": message.time.isoformat()
            })

        return APIResponse.success(data=decrypted_messages, message="Chat messages retrieved successfully.")

    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def delete_chat_message(user_id: str, message_id: str, db: Session):
    try:
        chat_message = db.query(ChatMessage).filter(ChatMessage.message_id == message_id).first()
        if not chat_message:
            raise APIError(status_code=404, detail="Chat message not found.")

        if chat_message.sender_id != user_id:
            raise APIError(status_code=403, detail="User not authorized to delete this message.")

        db.delete(chat_message)
        db.commit()

        return APIResponse.success(message="Chat message deleted successfully.")
    
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")
