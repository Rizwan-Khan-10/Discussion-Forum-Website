from sqlalchemy.orm import Session
from models.category import Category
from middlewares.encryption import EncryptionMiddleware
from middlewares.decryption import DecryptionMiddleware
import uuid

async def get_categories(db: Session):
    categories = db.query(Category).all()
    category_list = [
        {
            "category_id": category.category_id,
            "category_name": category.category_name,
            "description": category.description,
            "total_posts": category.total_posts
        }
        for category in categories
    ]
    
    return [DecryptionMiddleware.decrypt(cat) for cat in category_list]

async def add_category(request, db: Session):
    encrypted_data = EncryptionMiddleware.encrypt({
        "category_name": request.name,
        "description": request.description,
        "total_posts": "0"
    })
    
    new_category = Category(
        category_id=str(uuid.uuid4()),
        category_name=encrypted_data["category_name"],
        description=encrypted_data["description"],
        total_posts=encrypted_data["total_posts"]
    )
    
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    
    return {"message": "Category added successfully"}
