import uuid
from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  

class Post(Base):
    __tablename__ = "posts"
    
    post_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    category_id = Column(String, ForeignKey("categories.category_id"), nullable=False)
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    comments = Column(Integer, default=0)
    is_pinned = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    saved_threads = relationship("SavedThread", back_populates="post")

__all__ = [ "Post"]