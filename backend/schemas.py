from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List

class AttendanceSessionBase(BaseModel):
    check_in: datetime
    check_out: Optional[datetime] = None

class AttendanceSession(AttendanceSessionBase):
    id: int
    attendance_id: int

    class Config:
        from_attributes = True

class AttendanceBase(BaseModel):
    user_id: int = 1
    date: date
    status: str

class Attendance(AttendanceBase):
    id: int
    sessions: List[AttendanceSession] = []

    class Config:
        from_attributes = True

class AttendanceSummary(BaseModel):
    id: int
    date: date
    status: str
    effective_seconds: int
    gross_seconds: int
    break_seconds: int
    clock_in: Optional[datetime] = None
    clock_out: Optional[datetime] = None

class AttendanceStatus(BaseModel):
    status: str
    record: Optional[AttendanceSummary] = None
    server_time: datetime
    target_seconds: int = 28800  # 8 hours
