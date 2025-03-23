from sqlalchemy import Column, String, Integer, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  

class UserProfile(Base):
    __tablename__ = "user_profile"
    
    user_id = Column(String, ForeignKey("users.user_id"), primary_key=True)
    bio = Column(Text, nullable=True)
    img = Column(String, nullable=True)
    followers = Column(Integer, default=0)
    following = Column(Integer, default=0)
    total_posts = Column(Integer, default=0)
    total_upvotes = Column(Integer, default=0)
    total_downvotes = Column(Integer, default=0)
    reputation = Column(Integer, default=0)
    blockUser = Column(Boolean, default=False)
    blockCommunity = Column(Boolean, default=False)
    blockPost = Column(Boolean, default=False)
    
    user = relationship("User", back_populates="profile")

__all__ = [ "UserProfile"]