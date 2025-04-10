from sqlalchemy.orm import Session
from models.post import Post
from models.user import User
from models.followThread import FollowThread
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware
from datetime import datetime

async def addToFollowThread(post_id: str, user_id: str, db: Session):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise APIError(status_code=404, detail="User not found.")

        existing_follow = db.query(FollowThread).filter_by(post_id=post_id, user_id=user_id).first()

        decrypted = DecryptionMiddleware.decrypt({
            "followed": post.followed or EncryptionMiddleware.encrypt({"followed": "0"})["followed"]
        })
        current_count = int(decrypted.get("followed", "0"))

        if existing_follow:
            db.delete(existing_follow)
            new_count = max(0, current_count - 1)
            post.followed = EncryptionMiddleware.encrypt({"followed": str(new_count)})["followed"]
            db.commit()
            return APIResponse.success(message="Thread unfollowed.")
        else:
            new_follow = FollowThread(post_id=post_id, user_id=user_id, time=datetime.utcnow())
            db.add(new_follow)
            post.followed = EncryptionMiddleware.encrypt({"followed": str(current_count + 1)})["followed"]
            db.commit()
            return APIResponse.success(message="Thread followed.")
    except APIError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")


async def getFollowThread(post_id: str, user_id: str, db: Session):
    try:
        post = db.query(Post).filter_by(post_id=post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        follow = db.query(FollowThread).filter_by(post_id=post_id, user_id=user_id).first()
        is_following = bool(follow)

        decrypted = DecryptionMiddleware.decrypt({
            "followed": post.followed or EncryptionMiddleware.encrypt({"followed": "0"})["followed"]
        })
        follow_count = decrypted.get("followed", "0")

        return APIResponse.success(data={
            "is_following": is_following,
            "follow_count": follow_count
        })

    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")
