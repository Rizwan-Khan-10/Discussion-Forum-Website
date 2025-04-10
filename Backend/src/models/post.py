import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  

class Post(Base):
    __tablename__ = "posts"
    
    post_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    category_id = Column(String, ForeignKey("categories.category_id"), nullable=False)
    image_url = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    upvotes = Column(String, default="0")
    downvotes = Column(String, default="0")
    comment_count = Column(String, default="0") 
    bookmark_count = Column(String, default="0")
    shared = Column(String, default="0")
    report = Column(String, default="0")
    followed = Column(String, default="0")
    views = Column(String, default="0")
    is_pinned = Column(String, default="False")
    is_locked = Column(String, default="False")
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="posts")
    category = relationship("Category", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
    bookmark = relationship("Bookmark", back_populates="post")  
    followThread = relationship("FollowThread", back_populates="post") 

__all__ = ["Post"]
