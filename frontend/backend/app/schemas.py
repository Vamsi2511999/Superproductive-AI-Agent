# backend/app/schemas.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

class TaskBase(BaseModel):
    title: str
    source: Optional[str] = None
    source_ref: Optional[str] = None
    eta: Optional[date] = None
    priority: Optional[str] = None
    status: Optional[str] = "Pending"
    extracted_from: Optional[str] = None

class TaskCreate(TaskBase):
    pass

class Task(TaskBase):
    id: int
    class Config:
        orm_mode = True

class EmailItem(BaseModel):
    subject: str
    sender: Optional[str]
    email_body: str

class ToDoItem(BaseModel):
    task_title: str
    ETA_date: Optional[str]

class ExtractRequest(BaseModel):
    emails: Optional[List[EmailItem]] = None
    todos: Optional[List[ToDoItem]] = None

class ChatRequest(BaseModel):
    message: str
