from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from controllers.post_controller import (
    create_post, get_post_by_id, update_post,
    pin_post, lock_post, report_post, get_posts
)
from controllers.post_controller import PostRequest, UpdatePostRequest

post_router = APIRouter()

@post_router.post("/posts")
async def create_post_api(request: PostRequest, db: Session = Depends(get_db)):
    return await create_post(request, db)

@post_router.get("/posts/{post_id}")
async def get_post_by_id_api(post_id: str, db: Session = Depends(get_db)):
    return await get_post_by_id(post_id, db)

@post_router.put("/posts/{post_id}")
async def update_post_api(post_id: str, request: UpdatePostRequest, db: Session = Depends(get_db)):
    return await update_post(post_id, request, db)

@post_router.patch("/posts/{post_id}/pin")
async def pin_post_api(post_id: str, is_pinned: bool, db: Session = Depends(get_db)):
    return await pin_post(post_id, is_pinned, db)

@post_router.patch("/posts/{post_id}/lock")
async def lock_post_api(post_id: str, is_locked: bool, db: Session = Depends(get_db)):
    return await lock_post(post_id, is_locked, db)

@post_router.patch("/posts/{post_id}/report")
async def report_post_api(post_id: str, db: Session = Depends(get_db)):
    return await report_post(post_id, db)

@post_router.get("/posts")
async def get_random_or_category_posts_api(category_id: str = None, db: Session = Depends(get_db)):
    return await get_posts(category_id, db)
