from sqlalchemy.orm import Session
from models.communityComment import CommunityComment
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware
from pydantic import BaseModel
from datetime import datetime

class CommentRequest(BaseModel):
    post_id: str
    category_id: str
    user_id: str
    content: str

class VoteRequest(BaseModel):
    post_id: str
    category_id: str
    user_id: str
    vote_type: str 

async def add_comment(request: CommentRequest, db: Session):
    try:
        encrypted_content = EncryptionMiddleware.encrypt({"content": request.content})["content"]

        new_comment = CommunityComment(
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
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)

        return APIResponse.success(data=new_comment, message="Comment added successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def get_comments(post_id: str, category_id: str, db: Session):
    try:
        comments = db.query(CommunityComment).filter(CommunityComment.post_id == post_id, CommunityComment.category_id == category_id).all()
        if not comments:
            raise APIError(status_code=404, detail="No comments found.")

        decrypted_comments = []
        for comment in comments:
            decrypted_content = DecryptionMiddleware.decrypt({"content": comment.content})["content"]
            decrypted_comments.append({
                "post_id": comment.post_id,
                "category_id": comment.category_id,
                "user_id": comment.user_id,
                "content": decrypted_content,
                "upvotes": comment.upvotes,
                "downvotes": comment.downvotes,
                "replies": comment.replies,
                "is_pinned": comment.is_pinned,
                "created_at": comment.created_at
            })

        return APIResponse.success(data=decrypted_comments, message="Comments retrieved successfully.")

    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def edit_comment(post_id: str, category_id: str, content: str, db: Session):
    try:
        comment = db.query(CommunityComment).filter(CommunityComment.post_id == post_id, CommunityComment.category_id == category_id).first()
        if not comment:
            raise APIError(status_code=404, detail="Comment not found.")

        encrypted_content = EncryptionMiddleware.encrypt({"content": content})["content"]
        comment.content = encrypted_content

        db.commit()
        db.refresh(comment)

        return APIResponse.success(data=comment, message="Comment edited successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def delete_comment(post_id: str, category_id: str, db: Session):
    try:
        comment = db.query(CommunityComment).filter(CommunityComment.post_id == post_id, CommunityComment.category_id == category_id).first()
        if not comment:
            raise APIError(status_code=404, detail="Comment not found.")

        db.delete(comment)
        db.commit()

        return APIResponse.success(message="Comment deleted successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def vote_comment(request: VoteRequest, db: Session):
    try:
        comment = db.query(CommunityComment).filter(CommunityComment.post_id == request.post_id, CommunityComment.category_id == request.category_id).first()
        if not comment:
            raise APIError(status_code=404, detail="Comment not found.")

        if request.vote_type == "up":
            comment.upvotes += 1
        elif request.vote_type == "down":
            comment.downvotes += 1
        else:
            raise APIError(status_code=400, detail="Invalid vote type. Use 'up' or 'down'.")

        db.commit()
        db.refresh(comment)

        return APIResponse.success(data=comment, message=f"Comment {request.vote_type}voted successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")
