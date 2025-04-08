from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.post import Post
from models.user import User
from models.userProfile import UserProfile
from models.category import Category
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from pydantic import BaseModel
import datetime
import uuid
import os
from pathlib import Path
from typing import Optional
from fastapi import UploadFile
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware
from utils.cloudinary import upload_file, delete_file

class PostRequest(BaseModel):
    user_id: str
    title: str
    content: str
    category: str
    tags: Optional[str] = None

class UpdatePostRequest(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
TEMP_DIR = os.path.join(BASE_DIR, "backend", "public", "temp")
os.makedirs(TEMP_DIR, exist_ok=True)

async def create_post(request: PostRequest, postImage: UploadFile, db: Session):
    try:
        category_map = {
            "general": "General Discussion", "announcements": "Announcements",
            "questions": "Questions & Answers", "feedback": "Feedback & Suggestions",
            "support": "Technical Support", "guides": "Guides & Tutorials",
            "projects": "Projects & Showcases", "career": "Career / Jobs / Internships",
            "events": "Events / Meetups", "news": "News & Updates",
            "webdev": "Web Development", "appdev": "App Development",
            "gamedev": "Game Development", "ai_ml": "AI & Machine Learning",
            "cybersecurity": "Cybersecurity", "opensource": "Open Source",
            "programming": "Programming Help", "college": "College / Academics",
            "lifestyle": "Lifestyle & Wellness", "fun": "Memes / Fun", "offtopic": "Off Topic"
        }

        if request.category not in category_map:
            raise APIError(status_code=400, detail="Invalid category identifier.")

        actual_category_name = category_map[request.category]
        category = db.query(Category).filter_by(category_name=actual_category_name).first()
        if not category:
            raise APIError(status_code=400, detail="Category not found.")

        encrypted_fields = EncryptionMiddleware.encrypt({
            "title": request.title,
            "content": request.content,
            "tags": request.tags or ""
        })

        encrypted_defaults = EncryptionMiddleware.encrypt({
            "upvotes": "0", "downvotes": "0", "comment_count": "0",
            "bookmark": "0", "shared": "0", "report": "0", "followed": "0",
            "views": "0", "is_pinned": "False", "is_locked": "False"
        })

        post_id = str(uuid.uuid4())

        image_url = None
        if postImage:
            file_ext = os.path.splitext(postImage.filename)[-1]
            temp_path = os.path.join(TEMP_DIR, f"{post_id}{file_ext}")

            with open(temp_path, "wb") as f:
                content = await postImage.read()
                f.write(content)

            secure_url, _ = upload_file(temp_path, public_id=post_id)
            image_url = secure_url or None

            os.remove(temp_path)

        new_post = Post(
            post_id=post_id,
            user_id=request.user_id,
            title=encrypted_fields.get("title"),
            content=encrypted_fields.get("content"),
            category_id=category.category_id,
            tags=encrypted_fields.get("tags"),
            upvotes=encrypted_defaults.get("upvotes"),
            downvotes=encrypted_defaults.get("downvotes"),
            comment_count=encrypted_defaults.get("comment_count"),
            bookmark=encrypted_defaults.get("bookmark"),
            shared=encrypted_defaults.get("shared"),
            report=encrypted_defaults.get("report"),
            followed=encrypted_defaults.get("followed"),
            views=encrypted_defaults.get("views"),
            created_at=datetime.datetime.now(datetime.timezone.utc),
            updated_at=datetime.datetime.now(datetime.timezone.utc),
            image_url=EncryptionMiddleware.encrypt({"image_url": image_url}).get("image_url") if image_url else None
        )

        db.add(new_post)

        if category.total_posts is None:
            category.total_posts = "1"
        else:
            category.total_posts = str(int(category.total_posts) + 1)

        user_profile = db.query(UserProfile).filter_by(user_id=request.user_id).first()
        if user_profile:
            decrypted = DecryptionMiddleware.decrypt({
                "total_posts": user_profile.total_posts or EncryptionMiddleware.encrypt({"temp": "0"})["temp"],
                "reputation": user_profile.reputation or EncryptionMiddleware.encrypt({"temp": "0"})["temp"]
            })

            total_posts = int(decrypted.get("total_posts") or 0) + 1
            reputation = int(decrypted.get("reputation") or 0) + 5

            encrypted_updates = EncryptionMiddleware.encrypt({
                "total_posts": str(total_posts),
                "reputation": str(reputation)
            })

            user_profile.total_posts = encrypted_updates.get("total_posts")
            user_profile.reputation = encrypted_updates.get("reputation")

        db.commit()
        db.refresh(new_post)

        return APIResponse.success(data=serialize_post(new_post), message="Post created successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
def serialize_post(post):
    decrypted = DecryptionMiddleware.decrypt({
        "title": post.title,
        "content": post.content,
        "tags": post.tags,
        "upvotes": post.upvotes,
        "downvotes": post.downvotes,
        "comment_count": post.comment_count,
        "bookmark": post.bookmark,
        "shared": post.shared,
        "report": post.report,
        "followed": post.followed,
        "views": post.views
    })

    return {
        "post_id": post.post_id,
        "user_id": post.user_id,
        "title": decrypted.get("title"),
        "content": decrypted.get("content"),
        "category_id": post.category_id,
        "tags": decrypted.get("tags"),
        "upvotes": decrypted.get("upvotes"),
        "downvotes": decrypted.get("downvotes"),
        "comment_count": decrypted.get("comment_count"),
        "bookmark": decrypted.get("bookmark"),
        "shared": decrypted.get("shared"),
        "report": decrypted.get("report"),
        "followed": decrypted.get("followed"),
        "views": decrypted.get("views"),
        "created_at": post.created_at.isoformat() if post.created_at else None,
        "image_url": post.image_url
    }

async def get_post_by_id(user_id: str, db: Session):
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if not user:
            raise APIError(status_code=404, detail="User not found.")
        
        decrypted_user = DecryptionMiddleware.decrypt({
            "username": user.username
        })

        posts = db.query(Post).filter(Post.user_id == user_id).all()
        if not posts:
            return APIResponse.success(data=[], message="No posts found for this user.")

        result = []
        for post in posts:
            decrypted = DecryptionMiddleware.decrypt({
                "title": post.title,
                "content": post.content,
                "tags": post.tags or "",
                "image_url": post.image_url or "",
                "upvotes": post.upvotes,
                "downvotes": post.downvotes,
                "comment_count": post.comment_count,
                "bookmark": post.bookmark,
                "shared": post.shared,
                "report": post.report,
                "followed": post.followed,
                "views": post.views,
            })

            category_name = post.category.category_name  

            created_at = post.created_at.isoformat()
            updated_at = post.updated_at.isoformat()
            show_date = created_at if post.created_at == post.updated_at else updated_at

            post_data = {
                "user_id": user_id,
                "post_id": post.post_id,
                "user_id": user_id,
                "username": decrypted_user["username"], 
                "title": decrypted["title"],
                "content": decrypted["content"],
                "category_id": post.category_id,
                "category_name": category_name,
                "image_url": decrypted["image_url"],
                "tags": decrypted["tags"],
                "upvotes": decrypted["upvotes"],
                "downvotes": decrypted["downvotes"],
                "comment_count": decrypted["comment_count"],
                "bookmark": decrypted["bookmark"],
                "shared": decrypted["shared"],
                "report": decrypted["report"],
                "followed": decrypted["followed"],
                "views": decrypted["views"],
                "is_pinned": post.is_pinned,
                "is_locked": post.is_locked,
                "timestamp": show_date
            }

            result.append(post_data)

        return APIResponse.success(data=result, message="Posts retrieved successfully.")

    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def update_post(post_id: str, request: UpdatePostRequest, db: Session):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        request_data = request.model_dump(exclude_unset=True)
        encrypted_data = EncryptionMiddleware.encrypt(request_data)

        for key, value in encrypted_data.items():
            setattr(post, key, value)

        post.updated_at = datetime.datetime.utcnow()
        db.commit()
        db.refresh(post)

        return APIResponse.success(data=post, message="Post updated successfully.")
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def pin_post(post_id: str, is_pinned: str, db: Session):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        post.is_pinned = is_pinned  
        db.commit()

        return APIResponse.success(message=f"Post {'pinned' if is_pinned == 'True' else 'unpinned'} successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def lock_post(post_id: str, is_locked: str, db: Session):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        post.is_locked = is_locked  
        db.commit()

        return APIResponse.success(message=f"Post {'locked' if is_locked == 'True' else 'unlocked'} successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def delete_post(post_id: str, user_id: str, username: str, db: Session):
    try:
        post = db.query(Post).filter(Post.post_id == post_id, Post.user_id == user_id).first()
        
        if not post:
            raise APIError(status_code=404, detail="Post not found or you don't have permission to delete this post.")

        decrypted_username = DecryptionMiddleware.decrypt({"username": post.user.username})["username"]
        if decrypted_username != username:
            raise APIError(status_code=403, detail="Username mismatch. You are not authorized to delete this post.")

        delete_file(post_id)

        db.delete(post)
        db.commit()

        return APIResponse.success(data=[post_id],message="Post deleted successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def get_posts(category_id: str = None, db: Session = None):
    try:
        query = db.query(Post)

        if category_id:
            query = query.filter(Post.category_id == category_id)

        posts = query.order_by(func.random()).limit(10).all()  
        if not posts:
            raise APIError(status_code=404, detail="No posts found.")

        return APIResponse.success(data=posts, message="Posts retrieved successfully.")

    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")
