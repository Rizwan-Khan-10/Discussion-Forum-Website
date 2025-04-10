from sqlalchemy.orm import Session
from models.post import Post
from models.user import User
from models.userProfile import UserProfile
from models.comment import Comment 
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware
import uuid
import datetime

async def add_comment(request, db: Session):
    try:
        post = db.query(Post).filter_by(post_id=request.post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        user = db.query(User).filter_by(user_id=request.user_id).first()
        if not user:
            raise APIError(status_code=404, detail="User not found.")

        comment_id = str(uuid.uuid4())
        encrypted_content = EncryptionMiddleware.encrypt({"content": request.content})["content"]

        encrypted_defaults = EncryptionMiddleware.encrypt({
            "upvotes": "0", "downvotes": "0", "reply_count": "0"
        })

        current_time = datetime.datetime.now(datetime.timezone.utc)

        new_comment = Comment(
            comment_id=comment_id,
            post_id=request.post_id,
            user_id=request.user_id,
            content=encrypted_content,
            upvotes=encrypted_defaults["upvotes"],
            downvotes=encrypted_defaults["downvotes"],
            reply_count=encrypted_defaults["reply_count"],
            created_at=current_time
        )

        db.add(new_comment)
        db.commit()

        user_profile = db.query(UserProfile).filter_by(user_id=request.user_id).first()

        decrypted_username = DecryptionMiddleware.decrypt({"username": user.username}).get("username", user.username)
        decrypted_img = None
        if user_profile and user_profile.img:
            decrypted_img = DecryptionMiddleware.decrypt({"img": user_profile.img}).get("img", user_profile.img)

        response = {
            "comment_id": comment_id,
            "user_id": request.user_id,
            "username": decrypted_username,
            "img": decrypted_img,
            "content": request.content,
            "time": current_time.isoformat()
        }

        return APIResponse.success(message="Comment added successfully", data=response)

    except APIError as api_err:
        raise APIError(status_code=api_err.status_code, detail=api_err.detail)  

    except Exception as e:
        print("Error adding comment:", str(e))
        raise APIError(status_code=500, detail="An unexpected error occurred while adding comment.")

async def get_comments(post_id: str, db: Session):
    try:
        post = db.query(Post).filter_by(post_id=post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        comments = db.query(Comment).filter_by(post_id=post_id).order_by(Comment.created_at.asc()).all()

        response_data = []

        for comment in comments:
            user = db.query(User).filter_by(user_id=comment.user_id).first()
            user_profile = db.query(UserProfile).filter_by(user_id=comment.user_id).first()

            decrypted_username = user.username
            if user:
                decrypted_username = DecryptionMiddleware.decrypt({"username": user.username}).get("username", user.username)
            else:
                decrypted_username = "Unknown"

            decrypted_img = None
            if user_profile and user_profile.img:
                decrypted_img = DecryptionMiddleware.decrypt({"img": user_profile.img}).get("img", user_profile.img)

            decrypted_content = DecryptionMiddleware.decrypt({"content": comment.content}).get("content", comment.content)
            decrypted_upvotes = DecryptionMiddleware.decrypt({"upvotes": comment.upvotes}).get("upvotes", comment.upvotes)
            decrypted_downvotes = DecryptionMiddleware.decrypt({"downvotes": comment.downvotes}).get("downvotes", comment.downvotes)
            decrypted_reply_count = DecryptionMiddleware.decrypt({"reply_count": comment.reply_count}).get("reply_count", comment.reply_count)

            response_data.append({
                "comment_id": comment.comment_id,
                "user_id": comment.user_id,
                "username": decrypted_username,
                "img": decrypted_img,
                "content": decrypted_content,
                "upvotes": decrypted_upvotes,
                "downvotes": decrypted_downvotes,
                "reply_count": decrypted_reply_count,
                "time": comment.created_at
            })

        return APIResponse.success(message="Comments fetched successfully", data=response_data)

    except APIError as api_err:
        raise APIError(status_code=api_err.status_code, detail=api_err.detail)

    except Exception as e:
        print("Error fetching comments:", str(e))
        raise APIError(status_code=500, detail="An unexpected error occurred while fetching comments.")

async def delete_comment(post_id: str, comment_id: str, db: Session):
    try:
        post = db.query(Post).filter_by(post_id=post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        comment = db.query(Comment).filter_by(comment_id=comment_id, post_id=post_id).first()
        if not comment:
            raise APIError(status_code=404, detail="Comment not found.")

        db.delete(comment)
        db.commit()

        return APIResponse.success(message="Comment deleted successfully", data={"comment_id": comment_id})

    except APIError as api_err:
        raise APIError(status_code=api_err.status_code, detail=api_err.detail)

    except Exception as e:
        print("Error deleting comment:", str(e))
        raise APIError(status_code=500, detail="An unexpected error occurred while deleting comment.")

async def edit_comment(user_id: str, post_id: str, comment_id: str, new_content: str, db: Session):
    try:
        post = db.query(Post).filter_by(post_id=post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        user = db.query(User).filter_by(user_id=user_id).first()
        if not user:
            raise APIError(status_code=404, detail="User not found.")

        comment = db.query(Comment).filter_by(comment_id=comment_id, user_id=user_id, post_id=post_id).first()
        if not comment:
            raise APIError(status_code=404, detail="Comment not found or not authorized.")

        encrypted_content = EncryptionMiddleware.encrypt({"content": new_content})["content"]

        comment.content = encrypted_content
        current_time = datetime.datetime.now(datetime.timezone.utc)
        comment.created_at = current_time.isoformat() + " (edited)"

        db.commit()

        return APIResponse.success(message="Comment updated successfully", data={
            "comment_id": comment_id,
            "user_id": user_id,
            "content": new_content,
            "time": comment.created_at
        })

    except APIError as api_err:
        raise APIError(status_code=api_err.status_code, detail=api_err.detail)

    except Exception as e:
        print("Error editing comment:", str(e))
        raise APIError(status_code=500, detail="An unexpected error occurred while editing comment.")
