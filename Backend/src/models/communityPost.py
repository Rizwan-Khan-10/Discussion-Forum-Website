import uuid
from sqlalchemy import Column, String, Integer, Text, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  

class CommunityPost(Base):
    __tablename__ = "community_posts"
    
    community_post_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    community_id = Column(String, ForeignKey("communities.community_id"), nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    comments = Column(Integer, default=0)
    is_pinned = Column(Boolean, default=False)
    is_locked = Column(Boolean, default=False)
    upvotes = Column(Integer, default=0)
    downvotes = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="community_posts")
    community = relationship("Community", back_populates="community_posts")
    community_comments = relationship("CommunityComment", back_populates="community_post")

__all__ = [ "CommunityPost"]