from sqlalchemy.orm import Session
from models.communityReply import CommunityReply
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware
from pydantic import BaseModel
from datetime import datetime

class ReplyRequest(BaseModel):
    post_id: str
    category_id: str
    user_id: str
    content: str

class VoteRequest(BaseModel):
    post_id: str
    category_id: str
    user_id: str
    vote_type: str 

async def add_reply(request: ReplyRequest, db: Session):
    try:
        encrypted_content = EncryptionMiddleware.encrypt({"content": request.content})["content"]

        new_reply = CommunityReply(
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

        return APIResponse.success(data=new_reply, message="Reply added successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def get_replies(post_id: str, category_id: str, db: Session):
    try:
        replies = db.query(CommunityReply).filter(
            CommunityReply.post_id == post_id, 
            CommunityReply.category_id == category_id
        ).all()
        
        if not replies:
            raise APIError(status_code=404, detail="No replies found.")

        decrypted_replies = []
        for reply in replies:
            decrypted_content = DecryptionMiddleware.decrypt({"content": reply.content})["content"]
            decrypted_replies.append({
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

        return APIResponse.success(data=decrypted_replies, message="Replies retrieved successfully.")

    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def edit_reply(post_id: str, category_id: str, content: str, db: Session):
    try:
        reply = db.query(CommunityReply).filter(
            CommunityReply.post_id == post_id, 
            CommunityReply.category_id == category_id
        ).first()

        if not reply:
            raise APIError(status_code=404, detail="Reply not found.")

        encrypted_content = EncryptionMiddleware.encrypt({"content": content})["content"]
        reply.content = encrypted_content

        db.commit()
        db.refresh(reply)

        return APIResponse.success(data=reply, message="Reply edited successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def delete_reply(post_id: str, category_id: str, db: Session):
    try:
        reply = db.query(CommunityReply).filter(
            CommunityReply.post_id == post_id, 
            CommunityReply.category_id == category_id
        ).first()

        if not reply:
            raise APIError(status_code=404, detail="Reply not found.")

        db.delete(reply)
        db.commit()

        return APIResponse.success(message="Reply deleted successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def vote_reply(request: VoteRequest, db: Session):
    try:
        reply = db.query(CommunityReply).filter(
            CommunityReply.post_id == request.post_id, 
            CommunityReply.category_id == request.category_id
        ).first()

        if not reply:
            raise APIError(status_code=404, detail="Reply not found.")

        if request.vote_type == "up":
            reply.upvotes += 1
        elif request.vote_type == "down":
            reply.downvotes += 1
        else:
            raise APIError(status_code=400, detail="Invalid vote type. Use 'up' or 'down'.")

        db.commit()
        db.refresh(reply)

        return APIResponse.success(data=reply, message=f"Reply {request.vote_type}voted successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")
