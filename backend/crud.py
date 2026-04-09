from sqlalchemy.orm import Session
from datetime import datetime, date, time, timedelta, timezone
import models, schemas
from typing import List, Optional

def get_attendance_by_date(db: Session, user_id: int, target_date: date) -> Optional[models.Attendance]:
    return db.query(models.Attendance).filter(
        models.Attendance.user_id == user_id,
        models.Attendance.date == target_date
    ).first()

def get_history(db: Session, user_id: int, limit: int = 7) -> List[schemas.AttendanceSummary]:
    records = db.query(models.Attendance).filter(
        models.Attendance.user_id == user_id
    ).order_by(models.Attendance.date.desc()).limit(limit).all()
    
    return [calculate_summary(r) for r in records]

def calculate_summary(record: models.Attendance) -> schemas.AttendanceSummary:
    sessions = sorted(record.sessions, key=lambda s: s.check_in)
    
    effective_seconds = 0
    now = datetime.now(timezone.utc)
    
    for s in sessions:
        end = s.check_out if s.check_out else now
        effective_seconds += int((end - s.check_in).total_seconds())
    
    first_in = sessions[0].check_in if sessions else None
    last_out = sessions[-1].check_out if sessions and sessions[-1].check_out else (now if sessions else None)
    
    gross_seconds = 0
    if first_in:
        gross_seconds = int((last_out - first_in).total_seconds())
    
    break_seconds = max(0, gross_seconds - effective_seconds)
    
    return schemas.AttendanceSummary(
        id=record.id,
        date=record.date,
        status=record.status,
        effective_seconds=effective_seconds,
        gross_seconds=gross_seconds,
        break_seconds=break_seconds,
        clock_in=first_in,
        clock_out=sessions[-1].check_out if sessions else None
    )

def check_and_auto_close_previous(db: Session, user_id: int):
    today = date.today()
    open_attendances = db.query(models.Attendance).filter(
        models.Attendance.user_id == user_id,
        models.Attendance.date < today,
        models.Attendance.status == "Working"
    ).all()

    for attendance in open_attendances:
        open_session = db.query(models.AttendanceSession).filter(
            models.AttendanceSession.attendance_id == attendance.id,
            models.AttendanceSession.check_out == None
        ).first()
        
        if open_session:
            # Auto close at midnight of that day
            auto_time = datetime.combine(attendance.date, time(23, 59, 59), tzinfo=timezone.utc)
            open_session.check_out = auto_time
        
        attendance.status = "Completed"
    
    if open_attendances:
        db.commit()

def handle_check_in(db: Session, user_id: int):
    today = date.today()
    attendance = get_attendance_by_date(db, user_id, today)
    
    if not attendance:
        attendance = models.Attendance(user_id=user_id, date=today, status="Working")
        db.add(attendance)
        db.commit()
        db.refresh(attendance)
    
    # Ensure no session is currently open
    open_session = db.query(models.AttendanceSession).filter(
        models.AttendanceSession.attendance_id == attendance.id,
        models.AttendanceSession.check_out == None
    ).first()
    
    if not open_session:
        new_session = models.AttendanceSession(
            attendance_id=attendance.id,
            check_in=datetime.now(timezone.utc)
        )
        db.add(new_session)
        attendance.status = "Working"
        db.commit()
    
    return calculate_summary(attendance)

def handle_check_out(db: Session, user_id: int):
    today = date.today()
    attendance = get_attendance_by_date(db, user_id, today)
    
    if not attendance or attendance.status != "Working":
        return None
    
    open_session = db.query(models.AttendanceSession).filter(
        models.AttendanceSession.attendance_id == attendance.id,
        models.AttendanceSession.check_out == None
    ).first()
    
    if open_session:
        open_session.check_out = datetime.now(timezone.utc)
        attendance.status = "Break"
        db.commit()
    
    return calculate_summary(attendance)

def get_today_status(db: Session, user_id: int):
    check_and_auto_close_previous(db, user_id)
    today = date.today()
    attendance = get_attendance_by_date(db, user_id, today)
    
    if not attendance:
        return "Not Started", None
    
    summary = calculate_summary(attendance)
    return attendance.status, summary
