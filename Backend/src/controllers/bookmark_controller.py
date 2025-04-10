from sqlalchemy.orm import Session
from models.post import Post
from models.user import User
from models.userProfile import UserProfile
from models.bookmark import Bookmark
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware
from datetime import datetime

async def addToBookmark(post_id: str, user_id: str, db: Session):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise APIError(status_code=404, detail="User not found.")

        existing_bookmark = db.query(Bookmark).filter_by(post_id=post_id, user_id=user_id).first()

        # Decrypt bookmark_count
        decrypted = DecryptionMiddleware.decrypt({
            "bookmark_count": post.bookmark_count or EncryptionMiddleware.encrypt({"bookmark_count": "0"})["bookmark_count"]
        })
        current_count = int(decrypted.get("bookmark_count", "0"))

        if existing_bookmark:
            # Remove bookmark
            db.delete(existing_bookmark)
            new_count = max(0, current_count - 1)

            post.bookmark_count = EncryptionMiddleware.encrypt({
                "bookmark_count": str(new_count)
            })["bookmark_count"]

            await updateBookmark(db, user_id, "total_bookmarks", -1)

            db.commit()
            return APIResponse.success(message="Bookmark removed.")
        else:
            # Add bookmark
            new_bookmark = Bookmark(post_id=post_id, user_id=user_id, time=datetime.utcnow())
            db.add(new_bookmark)

            post.bookmark_count = EncryptionMiddleware.encrypt({
                "bookmark_count": str(current_count + 1)
            })["bookmark_count"]

            await updateBookmark(db, user_id, "total_bookmarks", 1)

            db.commit()
            return APIResponse.success(message="Bookmark added.")

    except APIError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")


async def getBookmark(post_id: str, user_id: str, db: Session):
    try:
        bookmark = db.query(Bookmark).filter_by(post_id=post_id, user_id=user_id).first()
        post = db.query(Post).filter_by(post_id=post_id).first()

        if not post:
            raise APIError(status_code=404, detail="Post not found")

        is_bookmarked = bool(bookmark)

        # Decrypt bookmark count
        decrypted = DecryptionMiddleware.decrypt({
            "bookmark_count": post.bookmark_count or EncryptionMiddleware.encrypt({"bookmark_count": "0"})["bookmark_count"]
        })

        bookmark_count = decrypted.get("bookmark_count", "0")

        return APIResponse.success(data={
            "is_bookmarked": is_bookmarked,
            "bookmark_count": bookmark_count
        })

    except APIError as e:
        raise e
    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")


async def updateBookmark(db: Session, user_id: str, field_name: str, increment: int):
    try:
        profile = db.query(UserProfile).filter_by(user_id=user_id).first()
        if profile:
            decrypted = DecryptionMiddleware.decrypt({
                field_name: getattr(profile, field_name) or EncryptionMiddleware.encrypt({field_name: "0"})[field_name]
            })
            current = int(decrypted.get(field_name, "0"))
            updated = max(0, current + increment)
            encrypted = EncryptionMiddleware.encrypt({field_name: str(updated)})[field_name]
            setattr(profile, field_name, encrypted)
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error during user profile update: {str(e)}")