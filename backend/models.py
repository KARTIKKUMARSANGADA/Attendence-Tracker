from sqlalchemy import Column, Integer, Date, DateTime, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True, default=1)
    date = Column(Date, index=True, unique=True)
    status = Column(String, default="Not Started") # "Working", "Break", "Completed"
    
    sessions = relationship("AttendanceSession", back_populates="attendance", cascade="all, delete-orphan")

class AttendanceSession(Base):
    __tablename__ = "attendance_sessions"

    id = Column(Integer, primary_key=True, index=True)
    attendance_id = Column(Integer, ForeignKey("attendance.id"))
    check_in = Column(DateTime(timezone=True))
    check_out = Column(DateTime(timezone=True), nullable=True)

    attendance = relationship("Attendance", back_populates="sessions")
