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
    tags = Column(String, nullable=True)
    upvotes = Column(String, nullable=True)
    downvotes = Column(String, nullable=True)
    comments = Column(String, nullable=True)
    bookmark = Column(String, nullable=True)
    shared = Column(String, nullable=True)
    report = Column(String, nullable=True)
    followed = Column(String, nullable=True)
    is_pinned = Column(String, default=False)
    is_locked = Column(String, default=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    saved_threads = relationship("SavedThread", back_populates="post")

__all__ = ["Post"]
