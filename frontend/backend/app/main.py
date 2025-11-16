# backend/app/main.py
import os
import json
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional
from app import models, schemas, crud
from app.database import SessionLocal, init_db, DB_FILE
from pathlib import Path
from datetime import datetime, timedelta
from pydantic import BaseModel

# initialize DB (creates SQLite file)
init_db()

app = FastAPI(title="Superproductive AI Agent - DB Backend")

# CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200", "http://127.0.0.1:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "mock_data"

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/tasks", response_model=list[schemas.Task])
def api_get_tasks(start: Optional[str] = None, end: Optional[str] = None, db: Session = Depends(get_db)):
    if not start and not end:
        tasks = crud.get_tasks(db)
        return tasks
    try:
        start_dt = None
        end_dt = None
        if start:
            start_dt = datetime.fromisoformat(start).date()
        if end:
            end_dt = datetime.fromisoformat(end).date()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid date format, use ISO YYYY-MM-DD")
    tasks = crud.get_tasks_by_date_range(db, start_dt, end_dt)
    return tasks

@app.post("/api/extract")
def api_extract(payload: schemas.ExtractRequest, db: Session = Depends(get_db)):
    added = crud.extract_and_store(db, emails=payload.emails, todos=payload.todos)
    return {"added_count": len(added), "added": added}

@app.post("/api/chat")
def api_chat(payload: schemas.ChatRequest, db: Session = Depends(get_db)):
    text = (payload.message or "").lower()
    now = datetime.utcnow().date()
    try:
        if "today" in text:
            res = [t for t in crud.get_tasks(db) if t.eta == now]
            return {"reply": f"You have {len(res)} task(s) due today.", "tasks": res}
        if "this week" in text:
            start = now
            end = now + timedelta(days=7)
            res = crud.get_tasks_by_date_range(db, start, end)
            return {"reply": f"You have {len(res)} task(s) due this week.", "tasks": res}
        if "summary" in text or "total" in text:
            all_tasks = crud.get_tasks(db)
            by_priority = {}
            for t in all_tasks:
                p = t.priority or "Unknown"
                by_priority[p] = by_priority.get(p, 0) + 1
            return {"reply": f"Total tasks: {len(all_tasks)}", "counts": {"total": len(all_tasks), "by_priority": by_priority}}
        # fallback
        pending = [t for t in crud.get_tasks(db) if t.status == "Pending"][:5]
        return {"reply": f"Here are your top {len(pending)} pending tasks.", "tasks": pending}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/reload-mock")
def api_reload_mock(db: Session = Depends(get_db)):
    # delete existing tasks and re-seed from mock files
    db.query(models.Task).delete()
    db.commit()
    # load todos
    todo_file = DATA_DIR / "todo_list.json"
    if todo_file.exists():
        with open(todo_file, "r", encoding="utf-8") as f:
            todos = json.load(f)
        crud.extract_and_store(db, emails=None, todos=[schemas.ToDoItem(**t) for t in todos])
    # load emails
    email_file = DATA_DIR / "emails.json"
    if email_file.exists():
        with open(email_file, "r", encoding="utf-8") as f:
            emails = json.load(f)
        crud.extract_and_store(db, emails=[schemas.EmailItem(**e) for e in emails], todos=None)
    count = db.query(models.Task).count()
    return {"status": "reloaded", "count": count}
