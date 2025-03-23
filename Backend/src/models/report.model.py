import uuid
from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from base import Base  

class Report(Base):
    __tablename__ = "reports"
    
    report_id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reported_by = Column(String, ForeignKey("users.user_id"), nullable=False)
    target_type = Column(String, nullable=False)
    target_id = Column(String, nullable=False)
    reason = Column(Text, nullable=False)
    status = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    
    reported_by_user = relationship("User", back_populates="reports")

__all__ = [ "Report"]