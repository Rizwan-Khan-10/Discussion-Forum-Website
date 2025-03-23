import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  

class SavedThread(Base):
    __tablename__ = "saved_threads"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    post_id = Column(String, ForeignKey("posts.post_id"), nullable=False)
    type = Column(String, nullable=False)
    time = Column(DateTime, nullable=False)
    
    user = relationship("User", back_populates="saved_threads")
    post = relationship("Post", back_populates="saved_threads")

__all__ = [ "SavedThread"]