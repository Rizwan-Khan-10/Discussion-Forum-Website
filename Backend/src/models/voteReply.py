from sqlalchemy import Column, String
from base import Base
import uuid

class ReplyVote(Base):
    __tablename__ = "replyVotes"
    
    vote_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reply_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    vote_type = Column(String, nullable=False)  

ReplyVote