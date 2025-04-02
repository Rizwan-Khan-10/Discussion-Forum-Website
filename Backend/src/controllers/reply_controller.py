from sqlalchemy.orm import Session
from models.reply import reply
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware
from pydantic import BaseModel
from datetime import datetime

class replyRequest(BaseModel):
    post_id: str
    category_id: str
    user_id: str
    content: str

class VoteRequest(BaseModel):
    post_id: str
    category_id: str
    user_id: str
    vote_type: str 

async def add_reply(request: replyRequest, db: Session):
    try:
        encrypted_content = EncryptionMiddleware.encrypt({"content": request.content})["content"]

        new_reply = reply(
            post_id=request.post_id,
            category_id=request.category_id,
            user_id=request.user_id,
            content=encrypted_content,
            upvotes=0,
            downvotes=0,
            replies=0,
            is_pinned=False,
            created_at=datetime.utcnow().isoformat()
        )
        db.add(new_reply)
        db.commit()
        db.refresh(new_reply)

        return APIResponse.success(data=new_reply, message="reply added successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def get_replys(post_id: str, category_id: str, db: Session):
    try:
        replys = db.query(reply).filter(reply.post_id == post_id, reply.category_id == category_id).all()
        if not replys:
            raise APIError(status_code=404, detail="No replys found.")

        decrypted_replys = []
        for reply in replys:
            decrypted_content = DecryptionMiddleware.decrypt({"content": reply.content})["content"]
            decrypted_replys.append({
                "post_id": reply.post_id,
                "category_id": reply.category_id,
                "user_id": reply.user_id,
                "content": decrypted_content,
                "upvotes": reply.upvotes,
                "downvotes": reply.downvotes,
                "replies": reply.replies,
                "is_pinned": reply.is_pinned,
                "created_at": reply.created_at
            })

        return APIResponse.success(data=decrypted_replys, message="replys retrieved successfully.")

    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def edit_reply(post_id: str, category_id: str, content: str, db: Session):
    try:
        reply = db.query(reply).filter(reply.post_id == post_id, reply.category_id == category_id).first()
        if not reply:
            raise APIError(status_code=404, detail="reply not found.")

        encrypted_content = EncryptionMiddleware.encrypt({"content": content})["content"]
        reply.content = encrypted_content

        db.commit()
        db.refresh(reply)

        return APIResponse.success(data=reply, message="reply edited successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def delete_reply(post_id: str, category_id: str, db: Session):
    try:
        reply = db.query(reply).filter(reply.post_id == post_id, reply.category_id == category_id).first()
        if not reply:
            raise APIError(status_code=404, detail="reply not found.")

        db.delete(reply)
        db.commit()

        return APIResponse.success(message="reply deleted successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def vote_reply(request: VoteRequest, db: Session):
    try:
        reply = db.query(reply).filter(reply.post_id == request.post_id, reply.category_id == request.category_id).first()
        if not reply:
            raise APIError(status_code=404, detail="reply not found.")

        if request.vote_type == "up":
            reply.upvotes += 1
        elif request.vote_type == "down":
            reply.downvotes += 1
        else:
            raise APIError(status_code=400, detail="Invalid vote type. Use 'up' or 'down'.")

        db.commit()
        db.refresh(reply)

        return APIResponse.success(data=reply, message=f"reply {request.vote_type}voted successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")
