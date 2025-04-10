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
    
    profile = relationship("UserProfile", back_populates="user", cascade="all, delete-orphan")
    posts = relationship("Post", back_populates="user", cascade="all, delete-orphan")
    comments = relationship("Comment", back_populates="user", cascade="all, delete-orphan")
    replies = relationship("Reply", back_populates="user", cascade="all, delete-orphan")
    community_users = relationship("CommunityUser", back_populates="user", cascade="all, delete-orphan")
    community_posts = relationship("CommunityPost", back_populates="user", cascade="all, delete-orphan")
    community_comments = relationship("CommunityComment", back_populates="user", cascade="all, delete-orphan")
    community_replies = relationship("CommunityReply", back_populates="user", cascade="all, delete-orphan")
    reports = relationship("Report", back_populates="reported_by_user", cascade="all, delete-orphan")
    personal_chats = relationship("PersonalChat", back_populates="user", cascade="all, delete-orphan")
    sent_messages = relationship("ChatMessage", foreign_keys="ChatMessage.sender_id", back_populates="sender", cascade="all, delete-orphan")
    received_messages = relationship("ChatMessage", foreign_keys="ChatMessage.receiver_id", back_populates="receiver", cascade="all, delete-orphan")
    bookmark = relationship("Bookmark", back_populates="user", cascade="all, delete-orphan")
    followThread = relationship("FollowThread", back_populates="user", cascade="all, delete-orphan")

__all__ = [ "User"]