import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  

class CommunityUser(Base):
    __tablename__ = "community_users"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    community_id = Column(String, ForeignKey("communities.community_id"), nullable=False)
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    role = Column(String, nullable=False)
    joined_at = Column(DateTime, nullable=False)
    
    community = relationship("Community", back_populates="community_users")
    user = relationship("User", back_populates="community_users")

__all__ = [ "CommunityUser"]