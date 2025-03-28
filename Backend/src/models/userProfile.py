from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  

class UserProfile(Base):
    __tablename__ = "user_profile"
    
    user_id = Column(String, ForeignKey("users.user_id"), primary_key=True)
    bio = Column(Text, nullable=True)
    img = Column(String, nullable=True)
    followers = Column(String, nullable=True)
    following = Column(String, nullable=True)
    total_posts = Column(String, nullable=True)
    total_upvotes = Column(String, nullable=True)
    total_downvotes = Column(String, nullable=True)
    reputation = Column(String, nullable=True)
    blockUser = Column(String, nullable=True)
    blockCommunity = Column(String, nullable=True)
    blockPost = Column(String, nullable=True)
    
    user = relationship("User", back_populates="profile")

__all__ = ["UserProfile"]
