from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum


class SourceType(str, Enum):
    EMAIL = "email"
    LOOP = "loop"
    TEAMS = "teams"


class PriorityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class TaskStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in-progress"
    COMPLETED = "completed"


class OutlookEmail(BaseModel):
    id: str
    subject: str
    sender: str
    sender_name: str
    body: str
    received_date: str
    has_attachments: bool


class LoopTask(BaseModel):
    id: str
    title: str
    description: str
    status: str
    priority: str
    due_date: str
    created_date: str
    assigned_to: str
    tags: List[str]


class TeamsMessage(BaseModel):
    id: str
    channel: str
    sender_name: str
    sender_email: str
    message: str
    timestamp: str
    mentions: List[str]
    reactions: List[str]


class ExtractedTask(BaseModel):
    id: str = Field(default_factory=lambda: f"task_{datetime.now().timestamp()}")
    title: str
    description: str
    source_type: SourceType
    source_id: str
    priority: PriorityLevel
    due_date: Optional[datetime] = None
    extracted_date: datetime = Field(default_factory=datetime.now)
    assigned_to: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING
    metadata: dict = {}


class TaskFilter(BaseModel):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    source_type: Optional[SourceType] = None
    priority: Optional[PriorityLevel] = None
    status: Optional[TaskStatus] = None


class ChatMessage(BaseModel):
    message: str
    context: Optional[dict] = None


class ChatResponse(BaseModel):
    response: str
    extracted_tasks: Optional[List[ExtractedTask]] = None
