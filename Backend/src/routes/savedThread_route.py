from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from pydantic import BaseModel
from controllers.savedThread_controller import add_saved_thread, get_saved_threads

saved_thread_router = APIRouter()

class SavedThreadRequest(BaseModel):
    user_id: str
    post_id: str
    type: str

@saved_thread_router.post("/add")
async def add_saved_thread_route(request: SavedThreadRequest, db: Session = Depends(get_db)):
    return await add_saved_thread(request, db)

@saved_thread_router.get("/get")
async def get_saved_threads_route(db: Session = Depends(get_db)):
    return await get_saved_threads(db)
