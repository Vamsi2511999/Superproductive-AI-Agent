# backend/app/models.py
from sqlalchemy import Column, Integer, String, Date, Text
from sqlalchemy.orm import relationship
from app.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    source = Column(String(32), nullable=True)       # "email", "todo", "teams"
    source_ref = Column(String(256), nullable=True)  # e.g. email subject or todo id
    eta = Column(Date, nullable=True)
    priority = Column(String(16), nullable=True)     # High/Medium/Low
    status = Column(String(32), nullable=False, default="Pending")
    extracted_from = Column(Text, nullable=True)     # snippet
