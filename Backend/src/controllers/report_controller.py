from sqlalchemy.orm import Session
from models.report import Report
from utils.ApiError import APIError
from utils.ApiResponse import APIResponse
from middlewares.encryption import EncryptionMiddleware
from pydantic import BaseModel
import uuid
from datetime import datetime

class ReportRequest(BaseModel):
    reported_by: str
    target_type: str
    target_id: str
    reason: str
    status: str

async def add_report(request: ReportRequest, db: Session):
    try:
        encrypted_reason = EncryptionMiddleware.encrypt({"reason": request.reason})["reason"]

        new_report = Report(
            report_id=str(uuid.uuid4()),
            reported_by=request.reported_by,
            target_type=request.target_type,
            target_id=request.target_id,
            reason=encrypted_reason,
            status=request.status,
            created_at=datetime.utcnow()
        )

        db.add(new_report)
        db.commit()
        db.refresh(new_report)

        return APIResponse.success(data=new_report, message="Report added successfully.")
    
    except Exception as e:
        db.rollback()
        raise APIError(status_code=500, detail=f"Internal Server Error: {str(e)}")
