from sqlalchemy.orm import Session
from models.personalChat import PersonalChat
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware
from pydantic import BaseModel
import uuid

class PersonalChatRequest(BaseModel):
    user_id: str
    user_list: dict
    last_message: dict | None = None

async def add_personal_chat(request: PersonalChatRequest, db: Session):
    try:
        encrypted_last_message = None
        if request.last_message:
            encrypted_last_message = EncryptionMiddleware.encrypt(request.last_message)
        
        new_chat = PersonalChat(
            chat_id=str(uuid.uuid4()),
            user_id=request.user_id,
            user_list=request.user_list,
            last_message=encrypted_last_message
        )
        
        db.add(new_chat)
        db.commit()
        db.refresh(new_chat)

        return APIResponse.success(data=new_chat, message="Personal chat added successfully.")
    
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def get_personal_chats(db: Session):
    try:
        chats = db.query(PersonalChat).all()
        if not chats:
            raise APIError(status_code=404, detail="No personal chats found.")

        decrypted_chats = []
        for chat in chats:
            decrypted_last_message = None
            if chat.last_message:
                decrypted_last_message = DecryptionMiddleware.decrypt(chat.last_message)
            
            decrypted_chats.append({
                "chat_id": chat.chat_id,
                "user_id": chat.user_id,
                "user_list": chat.user_list,
                "last_message": decrypted_last_message
            })

        return APIResponse.success(data=decrypted_chats, message="Personal chats retrieved successfully.")
    
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")
