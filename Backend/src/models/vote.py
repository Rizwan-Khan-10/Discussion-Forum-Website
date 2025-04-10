from sqlalchemy import Column, String
from base import Base
import uuid

class Vote(Base):
    __tablename__ = "votes"
    
    vote_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    post_id = Column(String, nullable=False)
    user_id = Column(String, nullable=False)
    vote_type = Column(String, nullable=False)  

__all__ = ["Vote"]