import uuid
from sqlalchemy import Column, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from base import Base  

class PersonalChat(Base):
    __tablename__ = "personal_chats"
    
    chat_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    user_list = Column(JSON, nullable=False)
    last_message = Column(JSON, nullable=True)
    
    user = relationship("User", back_populates="personal_chats")

__all__ = [ "PersonalChat" ]