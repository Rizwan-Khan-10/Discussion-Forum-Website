from sqlalchemy import Column, String
from base import Base
import uuid

class CommentVote(Base):
    __tablename__ = "commentVotes"
    
    vote_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    comment_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    vote_type = Column(String, nullable=False)  

__all__ = ["CommentVote"]