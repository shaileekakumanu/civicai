"""
Pydantic Schemas for CivicPulse APIs.
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class GrievanceAnalyzeRequest(BaseModel):
    text: str = Field(..., description="Citizen complaint text")
    ward_id: Optional[str] = None

class GrievanceSubmitRequest(BaseModel):
    text: str = Field(..., description="Citizen complaint text")
    citizen_name: Optional[str] = "Citizen"
    citizen_phone: Optional[str] = "+91 98765-43210"
    ward_id: Optional[str] = None
    landmark: Optional[str] = None

class TicketActionRequest(BaseModel):
    action: str = Field(..., description="Action: resolve, escalate, in_progress, reassign")
    officer_notes: Optional[str] = ""
    reassigned_dept: Optional[str] = None
