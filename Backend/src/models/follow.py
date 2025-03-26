from sqlalchemy import Column, String, ForeignKey
from base import Base

class Follower(Base):
    __tablename__ = "followers"

    user_id = Column(String, ForeignKey("users.user_id"), primary_key=True)  
    follower_id = Column(String, ForeignKey("users.user_id"), primary_key=True)  

__all__ = ["Follower"]
