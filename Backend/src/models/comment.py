import uuid
from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  

class Comment(Base):
    __tablename__ = "comments"
    
    comment_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = Column(String, ForeignKey("posts.post_id"), nullable=False)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    upvotes = Column(String, default=0)
    downvotes = Column(String, default=0)
    replies = Column(String, default=0)
    is_pinned = Column(String, default=False)
    created_at = Column(String, nullable=False)
    
    post = relationship("Post", back_populates="comments")
    user = relationship("User", back_populates="comments")
    replies = relationship("Reply", back_populates="comment")

__all__ = [ "Comment"]