import uuid
from sqlalchemy import Column, String, Integer, Text, DateTime
from sqlalchemy.orm import relationship
from base import Base  

class Community(Base):
    __tablename__ = "communities"
    
    community_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    members = Column(Integer, default=0)
    posts = Column(Integer, default=0)
    created_at = Column(DateTime, nullable=False)
    
    community_users = relationship("CommunityUser", back_populates="community")
    community_posts = relationship("CommunityPost", back_populates="community")

__all__ = [ "Community"]