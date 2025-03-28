from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from controllers.category_controller import get_categories, add_category
from pydantic import BaseModel

category_router = APIRouter()

class CategoryRequest(BaseModel):
    name: str
    description: str

@category_router.get("/categories")
async def fetch_categories(db: Session = Depends(get_db)):
    return await get_categories(db)

@category_router.post("/categories")
async def create_category(request: CategoryRequest, db: Session = Depends(get_db)):
    return await add_category(request, db)
