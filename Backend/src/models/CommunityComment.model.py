import uuid
from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  

class CommunityComment(Base):
    __tablename__ = "community_comments"
    
    comment_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    community_post_id = Column(String, ForeignKey("community_posts.community_post_id"), nullable=False)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    content = Column(Text, nullable=False)
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    replies = Column(Integer, default=0)
    is_pinned = Column(Boolean, default=False)
    created_at = Column(DateTime, nullable=False)
    
    community_post = relationship("CommunityPost", back_populates="community_comments")
    user = relationship("User", back_populates="community_comments")
    community_replies = relationship("CommunityReply", back_populates="community_comment")

__all__ = [ "CommunityComment"]