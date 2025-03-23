import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    
    message_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    receiver_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    sender_id = Column(String, ForeignKey("users.user_id"), nullable=False)
    message = Column(Text, nullable=False)
    time = Column(DateTime, nullable=False)
    
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_messages")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_messages")

__all__ = [ "ChatMessage"]