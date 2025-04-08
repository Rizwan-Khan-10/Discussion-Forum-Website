import uuid
from sqlalchemy import Column, String, Text
from sqlalchemy.orm import relationship
from base import Base  

class Category(Base):
    __tablename__ = "categories"
    
    category_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    category_name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    total_posts = Column(String, default=0)
    
    posts = relationship("Post", back_populates="category")

__all__ = [ "Category"]