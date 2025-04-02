from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.connection import get_db
from controllers.report_controller import add_report
from pydantic import BaseModel

report_router = APIRouter()

class ReportRequest(BaseModel):
    reported_by: str
    target_type: str
    target_id: str
    reason: str
    status: str

@report_router.post("/add")
async def add_report_route(request: ReportRequest, db: Session = Depends(get_db)):
    return await add_report(request, db)
