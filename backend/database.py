from sqlalchemy import create_engine, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/attendance_db")

# Auto-configure SSL for Supabase/Vercel serverless
if 'postgresql' in DATABASE_URL and '?' not in DATABASE_URL:
    DATABASE_URL += "?sslmode=require"

try:
    engine = create_engine(DATABASE_URL)

    # ✅ Test connection
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    logger.info("Database connected successfully")

except Exception as e:
    logger.error(f"Database connection failed: {str(e)}")
    raise

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()