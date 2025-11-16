# backend/app/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_FILE = os.path.join(BASE_DIR, "tasks.db")
DATABASE_URL = os.environ.get("DATABASE_URL") or f"sqlite:///{DB_FILE}"

# For SQLite, check_same_thread=False for multithreaded uvicorn
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def init_db():
    # Import models here to make sure they are registered
    from app import models  # noqa: F401
    Base.metadata.create_all(bind=engine)
