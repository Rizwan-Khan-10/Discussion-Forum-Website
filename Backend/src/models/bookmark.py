import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  

class Bookmark(Base):
    __tablename__ = "bookmarks"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    post_id = Column(String, ForeignKey("posts.post_id"), nullable=False)
    time = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="bookmark")
    post = relationship("Post", back_populates="bookmark")


__all__ = [ "Bookmark"]