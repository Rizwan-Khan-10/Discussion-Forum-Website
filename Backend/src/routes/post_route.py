from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from controllers.post_controller import (
    create_post, get_post_by_id,
    pin_post, lock_post, edit_post, fetch_popular_content, delete_post, count_view, get_bookmarked_posts ,get_followThread_posts
)
from controllers.post_controller import PostRequest
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

class EditRequest(BaseModel):
    post_id: str
    title: Optional[str] = None
    content: Optional[str] = None
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

class SavedPostRequest(BaseModel):
    user_id: str

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

@post_router.post("/pinUnpin")
async def pin_post_api(post_action: PostAction, db: Session = Depends(get_db)):
    return await pin_post(post_action.post_id, post_action.is_pinned, db)

@post_router.post("/blockUnblock")
async def lock_post_api(post_action: PostAction, db: Session = Depends(get_db)):
    return await lock_post(post_action.post_id, post_action.is_locked, db)

@post_router.post("/delete")
async def delete_post_api(delete_action: DeleteAction, db: Session = Depends(get_db)):
    return await delete_post(delete_action.post_id, delete_action.user_id, delete_action.username, db)

@post_router.post("/getBookmark")
async def get_bookmarked_posts_api(request: SavedPostRequest, db: Session = Depends(get_db)):
    return await get_bookmarked_posts(request.user_id, db)

@post_router.post("/getFollowedThread")
async def get_followedThread_posts_api(request: SavedPostRequest, db: Session = Depends(get_db)):
    return await get_followThread_posts(request.user_id, db)

@post_router.get("/Explore")
async def get_post_in_category_api(db: Session = Depends(get_db)):
    return await fetch_popular_content(db)

@post_router.post("/editPost")
async def edit_post_api(
    post_id: str = Form(...),
    title: str = Form(...),
    content: str = Form(...),
    category: str = Form(...),
    tags: str = Form(""), 
    postImage: UploadFile = File(None), 
    db: Session = Depends(get_db)
):
    request = EditRequest(
        post_id=post_id,
        title=title,
        content=content,
        category=category,
        tags=tags if tags else None,
    )
    return await edit_post(request, postImage, db)

@post_router.post("/countView")
async def count_view_api(
    payload: dict,
    db: Session = Depends(get_db)
):
    post_id = payload.get("post_id")
    user_id = payload.get("user_id")
    return await count_view(post_id, user_id, db)