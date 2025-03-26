import random
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func
from models.post import Post
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from pydantic import BaseModel
from datetime import datetime


class PostRequest(BaseModel):
    user_id: str
    title: str
    content: str
    category_id: str


class UpdatePostRequest(BaseModel):
    title: str = None
    content: str = None


async def create_post(request: PostRequest, db: Session):
    try:
        new_post = Post(
            user_id=request.user_id,
            title=request.title,
            content=request.content,
            category_id=request.category_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return APIResponse.success(data=new_post, message="Post created successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")


async def get_post_by_id(post_id: str, db: Session):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        return APIResponse.success(data=post, message="Post retrieved successfully.")

    except Exception as e:
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")


async def update_post(post_id: str, request: UpdatePostRequest, db: Session):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        post.title = request.title or post.title
        post.content = request.content or post.content
        post.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(post)

        return APIResponse.success(data=post, message="Post updated successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")


async def pin_post(post_id: str, is_pinned: bool, db: Session):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        post.is_pinned = is_pinned
        db.commit()
        return APIResponse.success(message=f"Post {'pinned' if is_pinned else 'unpinned'} successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")


async def lock_post(post_id: str, is_locked: bool, db: Session):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        post.is_locked = is_locked
        db.commit()
        return APIResponse.success(message=f"Post {'locked' if is_locked else 'unlocked'} successfully.")

    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")


async def report_post(post_id: str, db: Session):
    try:
        post = db.query(Post).filter(Post.post_id == post_id).first()
        if not post:
            raise APIError(status_code=404, detail="Post not found.")

        post.reports = post.reports + 1 if hasattr(post, 'reports') else 1
        db.commit()
        return APIResponse.success(message="Post reported successfully.")

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
