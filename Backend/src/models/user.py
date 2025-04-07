import uuid
from sqlalchemy import Column, String, Text, DateTime
from sqlalchemy.orm import relationship
from base import Base  

class User(Base):
    __tablename__ = "users"
    
    user_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(Text, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    profile = relationship("UserProfile", back_populates="user")
    posts = relationship("Post", back_populates="user")
    comments = relationship("Comment", back_populates="user")
    replies = relationship("Reply", back_populates="user")
    community_users = relationship("CommunityUser", back_populates="user")
    community_posts = relationship("CommunityPost", back_populates="user")
    community_comments = relationship("CommunityComment", back_populates="user")
    community_replies = relationship("CommunityReply", back_populates="user")
    reports = relationship("Report", back_populates="reported_by_user")
    personal_chats = relationship("PersonalChat", back_populates="user")
    sent_messages = relationship("ChatMessage", foreign_keys="ChatMessage.sender_id", back_populates="sender")
    received_messages = relationship("ChatMessage", foreign_keys="ChatMessage.receiver_id", back_populates="receiver")
    saved_threads = relationship("SavedThread", back_populates="user")

__all__ = [ "User"]