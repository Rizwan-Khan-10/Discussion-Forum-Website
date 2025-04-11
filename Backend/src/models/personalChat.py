import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from base import Base  

class PersonalChat(Base):
    __tablename__ = "personal_chats"
    
    chat_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    user_list = Column(JSONB, nullable=False)
    last_message = Column(JSONB, nullable=True)
    
    user = relationship("User", back_populates="personal_chats")

__all__ = [ "PersonalChat" ]