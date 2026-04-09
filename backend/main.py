from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timezone
import crud, models, schemas, database
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Standalone Attendance API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/status", response_model=schemas.AttendanceStatus)
def read_status(user_id: int = 1, db: Session = Depends(get_db)):
    status, summary = crud.get_today_status(db, user_id)
    return {
        "status": status,
        "record": summary,
        "server_time": datetime.now(timezone.utc),
        "target_seconds": 28800  # 8 hours
    }

@app.post("/check-in", response_model=schemas.AttendanceSummary)
def check_in(user_id: int = 1, db: Session = Depends(get_db)):
    status, _ = crud.get_today_status(db, user_id)
    if status == "Working":
        raise HTTPException(status_code=400, detail="Already checked in.")
    return crud.handle_check_in(db, user_id)

@app.post("/check-out", response_model=schemas.AttendanceSummary)
def check_out(user_id: int = 1, db: Session = Depends(get_db)):
    status, _ = crud.get_today_status(db, user_id)
    if status != "Working":
        raise HTTPException(status_code=400, detail="Not currently working.")
    return crud.handle_check_out(db, user_id)

@app.get("/history", response_model=list[schemas.AttendanceSummary])
def read_history(user_id: int = 1, db: Session = Depends(get_db)):
    return crud.get_history(db, user_id)
