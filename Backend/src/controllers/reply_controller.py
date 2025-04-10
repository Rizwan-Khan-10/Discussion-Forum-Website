from sqlalchemy.orm import Session
from models.reply import Reply
from models.user import User
from models.userProfile import UserProfile
from models.comment import Comment 
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware
import uuid
import datetime

async def add_reply(request, db: Session):
    try:
        comment = db.query(Comment).filter_by(comment_id=request.comment_id).first()
        if not comment:
            raise APIError(status_code=404, detail="Comment not found.")

        user = db.query(User).filter_by(user_id=request.user_id).first()
        if not user:
            raise APIError(status_code=404, detail="User not found.")

        reply_id = str(uuid.uuid4())
        encrypted_content = EncryptionMiddleware.encrypt({"content": request.content})["content"]
        current_time = datetime.datetime.now(datetime.timezone.utc)

        new_reply = Reply(
            reply_id=reply_id,
            comment_id=request.comment_id,
            user_id=request.user_id,
            content=encrypted_content,
            created_at=current_time
        )

        db.add(new_reply)
        db.commit()

        user_profile = db.query(UserProfile).filter_by(user_id=request.user_id).first()

        decrypted_username = DecryptionMiddleware.decrypt({"username": user.username}).get("username", user.username)
        decrypted_img = None
        if user_profile and user_profile.img:
            decrypted_img = DecryptionMiddleware.decrypt({"img": user_profile.img}).get("img", user_profile.img)

        response = {
            "comment_id": request.comment_id,
            "reply_id": reply_id,
            "user_id": request.user_id,
            "username": decrypted_username,
            "img": decrypted_img,
            "content": request.content,
            "time": current_time.isoformat()
        }

        return APIResponse.success(message="Reply added successfully", data=response)

    except APIError as api_err:
        raise api_err

    except Exception as e:
        print("Error adding reply:", str(e))
        raise APIError(status_code=500, detail="An unexpected error occurred while adding reply.")

async def get_replies(comment_id: str, db: Session):
    try:
        comment = db.query(Comment).filter_by(comment_id=comment_id).first()
        if not comment:
            raise APIError(status_code=404, detail="Comment not found.")

        replies = db.query(Reply).filter_by(comment_id=comment_id).order_by(Reply.created_at.asc()).all()

        response_data = []

        for reply in replies:
            user = db.query(User).filter_by(user_id=reply.user_id).first()
            user_profile = db.query(UserProfile).filter_by(user_id=reply.user_id).first()

            decrypted_username = DecryptionMiddleware.decrypt({"username": user.username}).get("username", user.username)
            decrypted_img = None
            if user_profile and user_profile.img:
                decrypted_img = DecryptionMiddleware.decrypt({"img": user_profile.img}).get("img", user_profile.img)

            decrypted_content = DecryptionMiddleware.decrypt({"content": reply.content}).get("content", reply.content)

            response_data.append({
                "comment_id": comment_id,
                "reply_id": reply.reply_id,
                "user_id": reply.user_id,
                "username": decrypted_username,
                "img": decrypted_img,
                "content": decrypted_content,
                "time": reply.created_at
            })

        return APIResponse.success(message="Replies fetched successfully", data=response_data)

    except APIError as api_err:
        raise api_err

    except Exception as e:
        print("Error fetching replies:", str(e))
        raise APIError(status_code=500, detail="An unexpected error occurred while fetching replies.")

async def delete_reply(comment_id: str, reply_id: str, db: Session):
    try:
        comment = db.query(Comment).filter_by(comment_id=comment_id).first()
        if not comment:
            raise APIError(status_code=404, detail="Comment not found.")

        reply = db.query(Reply).filter_by(reply_id=reply_id, comment_id=comment_id).first()
        if not reply:
            raise APIError(status_code=404, detail="Reply not found.")

        db.delete(reply)
        db.commit()

        return APIResponse.success(message="Reply deleted successfully", data={"reply_id": reply_id})

    except APIError as api_err:
        raise APIError(status_code=api_err.status_code, detail=api_err.detail)

    except Exception as e:
        print("Error deleting reply:", str(e))
        raise APIError(status_code=500, detail="An unexpected error occurred while deleting reply.")

async def edit_reply(user_id: str, comment_id: str, reply_id: str, new_content: str, db: Session):
    try:
        comment = db.query(Comment).filter_by(comment_id=comment_id).first()
        if not comment:
            raise APIError(status_code=404, detail="Comment not found.")

        user = db.query(User).filter_by(user_id=user_id).first()
        if not user:
            raise APIError(status_code=404, detail="User not found.")

        reply = db.query(Reply).filter_by(reply_id=reply_id, user_id=user_id, comment_id=comment_id).first()
        if not reply:
            raise APIError(status_code=404, detail="Reply not found or not authorized.")

        encrypted_content = EncryptionMiddleware.encrypt({"content": new_content})["content"]

        reply.content = encrypted_content
        current_time = datetime.datetime.now(datetime.timezone.utc)
        reply.created_at = current_time.isoformat() + " (edited)"

        db.commit()

        return APIResponse.success(message="Reply updated successfully", data={
            "reply_id": reply_id,
            "user_id": user_id,
            "content": new_content,
            "time": reply.created_at
        })

    except APIError as api_err:
        raise APIError(status_code=api_err.status_code, detail=api_err.detail)

    except Exception as e:
        print("Error editing reply:", str(e))
        raise APIError(status_code=500, detail="An unexpected error occurred while editing reply.")
