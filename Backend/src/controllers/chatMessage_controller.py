from sqlalchemy.orm import Session
from models.chatMessage import ChatMessage
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware
from pydantic import BaseModel
from datetime import datetime

class ChatMessageRequest(BaseModel):
    receiver_id: str
    sender_id: str
    message: str
    time: str  

async def add_chat_message(request: ChatMessageRequest, db: Session):
    try:
        encrypted_message = EncryptionMiddleware.encrypt({"message": request.message})["message"]
        
        new_message = ChatMessage(
            receiver_id=request.receiver_id,
            sender_id=request.sender_id,
            message=encrypted_message,
            time=request.time
        )
        db.add(new_message)
        db.commit()
        db.refresh(new_message)

        return APIResponse.success(data=new_message, message="Chat message added successfully.")
    
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def get_chat_messages(db: Session):
    try:
        messages = db.query(ChatMessage).all()
        if not messages:
            raise APIError(status_code=404, detail="No chat messages found.")

        decrypted_messages = []
        for message in messages:
            decrypted_content = DecryptionMiddleware.decrypt({"message": message.message})["message"]
            decrypted_messages.append({
                "message_id": message.message_id,
                "receiver_id": message.receiver_id,
                "sender_id": message.sender_id,
                "message": decrypted_content,
                "time": message.time
            })

        return APIResponse.success(data=decrypted_messages, message="Chat messages retrieved successfully.")
    
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def edit_chat_message(message_id: str, message: str, db: Session):
    try:
        chat_message = db.query(ChatMessage).filter(ChatMessage.message_id == message_id).first()
        if not chat_message:
            raise APIError(status_code=404, detail="Chat message not found.")

        encrypted_message = EncryptionMiddleware.encrypt({"message": message})["message"]
        chat_message.message = encrypted_message

        db.commit()
        db.refresh(chat_message)

        return APIResponse.success(data=chat_message, message="Chat message edited successfully.")
    
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def delete_chat_message(message_id: str, db: Session):
    try:
        chat_message = db.query(ChatMessage).filter(ChatMessage.message_id == message_id).first()
        if not chat_message:
            raise APIError(status_code=404, detail="Chat message not found.")

        db.delete(chat_message)
        db.commit()

        return APIResponse.success(message="Chat message deleted successfully.")
    
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")