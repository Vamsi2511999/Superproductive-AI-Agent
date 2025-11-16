import json
import os
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.models import (
    OutlookEmail,
    LoopTask,
    TeamsMessage,
    ExtractedTask,
    TaskFilter,
    ChatMessage,
    ChatResponse,
    SourceType,
    PriorityLevel,
    TaskStatus,
)
from app.ai_engine import AIEngine

app = FastAPI(title="Superproductive AI Agent API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize AI Engine
ai_engine = AIEngine()

# In-memory storage for extracted tasks
extracted_tasks: List[ExtractedTask] = []

# Data paths
DATA_DIR = Path(__file__).parent.parent / "data"


def load_json_data(filename: str):
    """Load JSON data from file"""
    filepath = DATA_DIR / filename
    if not filepath.exists():
        return []
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)


@app.get("/")
async def root():
    return {
        "message": "Superproductive AI Agent API",
        "version": "1.0.0",
        "endpoints": {
            "tasks": "/api/tasks",
            "extract": "/api/tasks/extract",
            "prioritize": "/api/tasks/prioritize",
            "filter": "/api/tasks/filter",
            "chat": "/api/chat",
            "insights": "/api/insights",
        },
    }


@app.get("/api/tasks", response_model=List[ExtractedTask])
async def get_tasks():
    """Get all extracted tasks"""
    return extracted_tasks


@app.post("/api/tasks/extract")
async def extract_tasks():
    """Extract tasks from all data sources"""
    global extracted_tasks
    extracted_tasks = []

    try:
        # Load data from files
        emails_data = load_json_data("outlook_emails.json")
        loop_data = load_json_data("loop_tasks.json")
        teams_data = load_json_data("teams_messages.json")

        # Extract from emails
        for email_data in emails_data:
            email = OutlookEmail(**email_data)
            tasks = ai_engine.extract_tasks_from_email(email)
            extracted_tasks.extend(tasks)

        # Convert Loop tasks
        for loop_data_item in loop_data:
            loop_task = LoopTask(**loop_data_item)
            task = ai_engine.convert_loop_task(loop_task)
            extracted_tasks.append(task)

        # Extract from Teams messages
        for teams_data_item in teams_data:
            teams_msg = TeamsMessage(**teams_data_item)
            tasks = ai_engine.extract_tasks_from_teams(teams_msg)
            extracted_tasks.extend(tasks)

        return {
            "message": "Tasks extracted successfully",
            "total_tasks": len(extracted_tasks),
            "by_source": {
                "email": len([t for t in extracted_tasks if t.source_type == SourceType.EMAIL]),
                "loop": len([t for t in extracted_tasks if t.source_type == SourceType.LOOP]),
                "teams": len([t for t in extracted_tasks if t.source_type == SourceType.TEAMS]),
            },
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error extracting tasks: {str(e)}")


@app.post("/api/tasks/prioritize")
async def prioritize_tasks():
    """Prioritize all extracted tasks using AI"""
    global extracted_tasks

    if not extracted_tasks:
        raise HTTPException(
            status_code=400,
            detail="No tasks to prioritize. Please extract tasks first.",
        )

    try:
        extracted_tasks = ai_engine.prioritize_tasks(extracted_tasks)
        return {
            "message": "Tasks prioritized successfully",
            "total_tasks": len(extracted_tasks),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error prioritizing tasks: {str(e)}")


@app.get("/api/tasks/filter", response_model=List[ExtractedTask])
async def filter_tasks(
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    source_type: Optional[SourceType] = Query(None),
    priority: Optional[PriorityLevel] = Query(None),
    status: Optional[TaskStatus] = Query(None),
):
    """Filter tasks based on various criteria"""
    filtered = extracted_tasks

    # Filter by date range
    if start_date:
        try:
            # Handle both YYYY-MM-DD format from UI and ISO format
            if 'T' in start_date:
                start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
            else:
                # Convert YYYY-MM-DD to datetime at 00:00:00
                start_dt = datetime.fromisoformat(start_date + "T00:00:00")
        except:
            start_dt = datetime.fromisoformat(start_date.replace("Z", "+00:00"))
        
        # Safe date comparison - strip timezone for comparison
        filtered = [
            t for t in filtered if t.due_date and (
                (t.due_date.replace(tzinfo=None) if t.due_date.tzinfo else t.due_date) >= start_dt.replace(tzinfo=None)
            )
        ]

    if end_date:
        try:
            # Handle both YYYY-MM-DD format from UI and ISO format
            if 'T' in end_date:
                end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
            else:
                # Convert YYYY-MM-DD to datetime at 23:59:59
                end_dt = datetime.fromisoformat(end_date + "T23:59:59")
        except:
            end_dt = datetime.fromisoformat(end_date.replace("Z", "+00:00"))
        
        # Safe date comparison - strip timezone for comparison
        filtered = [
            t for t in filtered if t.due_date and (
                (t.due_date.replace(tzinfo=None) if t.due_date.tzinfo else t.due_date) <= end_dt.replace(tzinfo=None)
            )
        ]

    # Filter by source type
    if source_type:
        filtered = [t for t in filtered if t.source_type == source_type]

    # Filter by priority
    if priority:
        filtered = [t for t in filtered if t.priority == priority]

    # Filter by status
    if status:
        filtered = [t for t in filtered if t.status == status]

    return filtered


@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Chat interface for task-related queries"""
    try:
        # Pass current tasks as context for better responses
        if not extracted_tasks:
            response = "You don't have any tasks yet. Please extract tasks from your emails, Teams, or Loop first."
        else:
            response = ai_engine.chat_interface(message.message, extracted_tasks)
        return ChatResponse(response=response, extracted_tasks=None)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")


@app.get("/api/insights")
async def get_insights():
    """Get AI-generated insights about tasks"""
    if not extracted_tasks:
        return {"message": "No tasks available. Please extract tasks first."}

    try:
        insights = ai_engine.generate_task_insights(extracted_tasks)
        return insights
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating insights: {str(e)}")


@app.delete("/api/tasks/{task_id}")
async def delete_task(task_id: str):
    """Delete a specific task"""
    global extracted_tasks
    initial_count = len(extracted_tasks)
    extracted_tasks = [t for t in extracted_tasks if t.id != task_id]

    if len(extracted_tasks) == initial_count:
        raise HTTPException(status_code=404, detail="Task not found")

    return {"message": "Task deleted successfully"}


@app.put("/api/tasks/{task_id}/status")
async def update_task_status(task_id: str, status: TaskStatus):
    """Update task status"""
    for task in extracted_tasks:
        if task.id == task_id:
            task.status = status
            return {"message": "Task status updated", "task": task}

    raise HTTPException(status_code=404, detail="Task not found")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
