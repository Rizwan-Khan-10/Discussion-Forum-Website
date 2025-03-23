import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  

class CommunityReply(Base):
    __tablename__ = "community_replies"
    
    reply_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    comment_id = Column(String, ForeignKey("community_comments.comment_id"), nullable=False)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=False)
    
    community_comment = relationship("CommunityComment", back_populates="community_replies")
    user = relationship("User", back_populates="community_replies")

__all__ = [ "CommunityReply"]