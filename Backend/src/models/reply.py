import uuid
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  

class Reply(Base):
    __tablename__ = "replies"
    
    reply_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    comment_id = Column(String, ForeignKey("comments.comment_id"), nullable=False)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    upvotes = Column(String, default=0)
    downvotes = Column(String, default=0)
    created_at = Column(String, nullable=False)
    
    comment = relationship("Comment", back_populates="replies")
    user = relationship("User", back_populates="replies")

__all__ = [ "Reply" ]