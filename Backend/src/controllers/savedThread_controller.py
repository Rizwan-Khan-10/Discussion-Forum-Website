import uuid
from sqlalchemy.orm import Session
from models.savedThread import SavedThread
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware
from pydantic import BaseModel
from datetime import datetime, timezone

class SavedThreadRequest(BaseModel):
    user_id: str
    post_id: str
    type: str

async def add_saved_thread(request: SavedThreadRequest, db: Session):
    try:
        encrypted_request = EncryptionMiddleware.encrypt(request.dict())

        new_saved_thread = SavedThread(
            id=str(uuid.uuid4()),
            user_id=encrypted_request["user_id"],
            post_id=encrypted_request["post_id"],
            type=encrypted_request["type"],
            time=datetime.now(timezone.utc)
        )

        db.add(new_saved_thread)
        db.commit()
        db.refresh(new_saved_thread)

        return APIResponse.success(data=new_saved_thread, message="Thread saved successfully.")
    
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def get_saved_threads(db: Session):
    try:
        saved_threads = db.query(SavedThread).all()
        if not saved_threads:
            raise APIError(status_code=404, detail="No saved threads found.")

        decrypted_threads = [
            DecryptionMiddleware.decrypt({
                "id": thread.id,
                "user_id": thread.user_id,
                "post_id": thread.post_id,
                "type": thread.type,
                "time": thread.time
            }) for thread in saved_threads
        ]

        return APIResponse.success(data=decrypted_threads, message="Saved threads retrieved successfully.")
    
    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")
