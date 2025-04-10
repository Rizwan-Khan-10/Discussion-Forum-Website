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

class EditRequest(BaseModel):
    post_id: str
    title: Optional[str] = None
    content: Optional[str] = None
    category: str
    tags: Optional[str] = None

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
            "bookmark_count": "0", "shared": "0", "report": "0", "followed": "0",
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
            bookmark_count=encrypted_defaults.get("bookmark_count"),
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
        import traceback
        print("Error while creating post:", traceback.format_exc())
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")
    
def serialize_post(post):
    decrypted = DecryptionMiddleware.decrypt({
        "title": post.title,
        "content": post.content,
        "tags": post.tags,
        "upvotes": post.upvotes,
        "downvotes": post.downvotes,
        "comment_count": post.comment_count,
        "bookmark_count": post.bookmark_count,
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
        "bookmark_count": decrypted.get("bookmark_count"),
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
                "bookmark_count": post.bookmark_count,
                "shared": post.shared,
                "report": post.report,
                "followed": post.followed,
                "views": post.views,
            })

            category_name = post.category.category_name  

            created_at = post.created_at.isoformat()
            updated_at = post.updated_at.isoformat()
            show_date = created_at if post.created_at == post.updated_at else updated_at
            edited = post.created_at == post.updated_at

            post_data = {
                "user_id": user_id,
                "post_id": post.post_id,
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
                "bookmark_count": decrypted["bookmark_count"],
                "shared": decrypted["shared"],
                "report": decrypted["report"],
                "followed": decrypted["followed"],
                "views": decrypted["views"],
                "is_pinned": post.is_pinned,
                "is_locked": post.is_locked,
                "timestamp": show_date,
                "edited": edited
            }

            result.append(post_data)

        return APIResponse.success(data=result, message="Posts retrieved successfully.")

    except Exception as e:
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

        image_url = DecryptionMiddleware.decrypt({"image_url": post.image_url}).get("image_url") if post.image_url else None
        if image_url and "cloudinary" in image_url:
            delete_file(post_id)

        upvotes = int(DecryptionMiddleware.decrypt({"val": post.upvotes}).get("val", "0")) if post.upvotes else 0
        downvotes = int(DecryptionMiddleware.decrypt({"val": post.downvotes}).get("val", "0")) if post.downvotes else 0
        bookmarks = int(DecryptionMiddleware.decrypt({"val": post.bookmark_count}).get("val", "0")) if post.bookmark_count else 0
        shares = int(DecryptionMiddleware.decrypt({"val": post.shared}).get("val", "0")) if post.shared else 0
        views = int(DecryptionMiddleware.decrypt({"val": post.views}).get("val", "0")) if post.views else 0

        user_profile = db.query(UserProfile).filter_by(user_id=user_id).first()
        if user_profile:
            fields_to_decrement = {
                "total_posts": 1,
                "total_upvotes": upvotes,
                "total_downvotes": downvotes,
                "total_bookmarks": bookmarks,
                "total_shares": shares,
                "total_views": views,
                "reputation": 5  
            }

            updated_data = {}
            for field, minus_value in fields_to_decrement.items():
                encrypted_val = getattr(user_profile, field)
                decrypted_val = DecryptionMiddleware.decrypt({
                    field: encrypted_val or EncryptionMiddleware.encrypt({field: "0"})[field]
                }).get(field, "0")

                new_val = max(0, int(decrypted_val) - minus_value)
                encrypted_new_val = EncryptionMiddleware.encrypt({field: str(new_val)}).get(field)
                setattr(user_profile, field, encrypted_new_val)

        db.delete(post)
        db.commit()

        return APIResponse.success(data=[post_id], message="Post deleted successfully.")

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

async def edit_post(request: EditRequest, postImage: UploadFile, db: Session):
    try:
        post = db.query(Post).filter_by(post_id=request.post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

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

        updated_fields = {}
        if request.title:
            updated_fields["title"] = request.title
        if request.content:
            updated_fields["content"] = request.content

        if request.tags is None:
            post.tags = None
        elif request.tags is not None:
            encrypted_tags = EncryptionMiddleware.encrypt({"tags": request.tags})
            post.tags = encrypted_tags.get("tags")

        image_url_encrypted = post.image_url
        image_url = DecryptionMiddleware.decrypt({"image_url": image_url_encrypted}).get("image_url") if image_url_encrypted else None
        delete_old_image = False

        if postImage:
            file_ext = os.path.splitext(postImage.filename)[-1]
            BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
            TEMP_DIR = os.path.join(BASE_DIR, "backend", "public", "temp")
            os.makedirs(TEMP_DIR, exist_ok=True)

            temp_path = os.path.join(TEMP_DIR, f"{request.post_id}{file_ext}")
            with open(temp_path, "wb") as f:
                content = await postImage.read()
                f.write(content)

            public_id = f"post_images/{request.post_id}"
            secure_url, _ = upload_file(temp_path, public_id=public_id)
            os.remove(temp_path)

            if secure_url:
                if image_url and "cloudinary" in image_url:
                    delete_file(f"post_images/{request.post_id}")
                image_url = secure_url

        elif postImage is None and image_url:
            if "cloudinary" in image_url:
                delete_file(f"post_images/{request.post_id}")
            image_url = None

        if updated_fields:
            encrypted_updated_fields = EncryptionMiddleware.encrypt(updated_fields)
            for field, value in encrypted_updated_fields.items():
                setattr(post, field, value)

        post.category_id = category.category_id
        post.image_url = (
            EncryptionMiddleware.encrypt({"image_url": image_url}).get("image_url")
            if image_url is not None else None
        )
        post.updated_at = datetime.datetime.now(datetime.timezone.utc)

        db.commit()
        db.refresh(post)

        response_data = {"post_id": post.post_id}
        if "title" in updated_fields:
            response_data["title"] = updated_fields["title"]
        if "content" in updated_fields:
            response_data["content"] = updated_fields["content"]
        if request.tags is not None:
            response_data["tags"] = request.tags
        elif request.tags is None:
            response_data["tags"] = None
        if image_url is not None:
            response_data["image_url"] = image_url
        elif image_url is None:
            response_data["image_url"] = None

        return APIResponse.success(data=response_data, message="Post edited successfully.")
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")

async def count_view(post_id: str, user_id: str, db: Session):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        post_views_encrypted = post.views or EncryptionMiddleware.encrypt({"views": "0"})["views"]
        post_views_decrypted = DecryptionMiddleware.decrypt({"views": post_views_encrypted})
        current_post_views = int(post_views_decrypted.get("views", "0"))
        new_post_views = current_post_views + 1
        post.views = EncryptionMiddleware.encrypt({"views": str(new_post_views)}).get("views")

        user = db.query(User).filter(User.user_id == user_id).first()
        new_user_views = None

        if user:
            user_profile = db.query(UserProfile).filter_by(user_id=user_id).first()
            if user_profile:
                profile_views_encrypted = user_profile.total_views or EncryptionMiddleware.encrypt({"total_views": "0"})["total_views"]
                profile_views_decrypted = DecryptionMiddleware.decrypt({"total_views": profile_views_encrypted})
                current_user_views = int(profile_views_decrypted.get("total_views", "0"))
                new_user_views = current_user_views + 1
                user_profile.total_views = EncryptionMiddleware.encrypt({"total_views": str(new_user_views)}).get("total_views")

        db.commit()

        return APIResponse.success(
            data=[new_post_views],
            message="View count updated successfully."
        )

    except APIError as e:
        db.rollback()
        raise e
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")
