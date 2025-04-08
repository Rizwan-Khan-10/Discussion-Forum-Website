from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from controllers.post_controller import (
    create_post, get_post_by_id, update_post,
    pin_post, lock_post, report_post, get_posts,delete_post
)
from controllers.post_controller import PostRequest, UpdatePostRequest
from pydantic import BaseModel
from fastapi import Form, File, UploadFile
from typing import Optional

post_router = APIRouter()

class PostRequest(BaseModel):
    user_id: str
    title: str
    content: str
    category: str
    tags: Optional[str] = None

class PostAction(BaseModel):
    post_id: str
    is_pinned: str 
    is_locked: str  

class DeleteAction(BaseModel):
    post_id: str
    user_id: str 
    username: str  

@post_router.post("/addPost")
async def create_post_api(
    user_id: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    category: str = Form(...),
    tags: str = Form(""), 
    postImage: UploadFile = File(None), 
    db: Session = Depends(get_db)
):
    request = PostRequest(
        user_id=user_id,
        title=title,
        content=content,
        category=category,
        tags=tags if tags else None,
    )
    return await create_post(request, postImage, db)

@post_router.post("/getPost")
async def get_post_by_id_api(payload: dict, db: Session = Depends(get_db)):
    user_id = payload.get("user_id")
    return await get_post_by_id(user_id, db)

@post_router.put("/posts/{post_id}")
async def update_post_api(post_id: str, request: UpdatePostRequest, db: Session = Depends(get_db)):
    return await update_post(post_id, request, db)

@post_router.post("/pinUnpin")
async def pin_post_api(post_action: PostAction, db: Session = Depends(get_db)):
    return await pin_post(post_action.post_id, post_action.is_pinned, db)

@post_router.post("/blockUnblock")
async def lock_post_api(post_action: PostAction, db: Session = Depends(get_db)):
    return await lock_post(post_action.post_id, post_action.is_locked, db)

@post_router.post("/delete")
async def delete_post_api(delete_action: DeleteAction, db: Session = Depends(get_db)):
    return await delete_post(delete_action.post_id, delete_action.user_id, delete_action.username, db)

@post_router.get("/posts")
async def get_random_or_category_posts_api(category_id: str = None, db: Session = Depends(get_db)):
    return await get_posts(category_id, db)
