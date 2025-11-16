# backend/app/crud.py
from sqlalchemy.orm import Session
from app import models, schemas
from typing import List, Optional
from datetime import date, datetime, timedelta
from dateutil import parser as dateparser

PRIORITY_KEYWORDS = {
    "High": ["urgent", "asap", "eod", "today", "immediately", "right away"],
    "Medium": ["soon", "this week", "next week", "by"],
    "Low": ["optional", "fyi", "when possible"]
}

def parse_eta(text: str) -> Optional[date]:
    text = (text or "").lower()
    today = datetime.utcnow().date()
    if "today" in text or "eod" in text or "by today" in text:
        return today
    if "tomorrow" in text:
        return today + timedelta(days=1)
    weekdays = ["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
    for i, d in enumerate(weekdays):
        if d in text:
            target = i
            days_ahead = (target - today.weekday() + 7) % 7
            if days_ahead == 0:
                days_ahead = 7
            return today + timedelta(days=days_ahead)
    # fuzzy parse
    try:
        dt = dateparser.parse(text, fuzzy=True, dayfirst=False)
        if dt:
            return dt.date()
    except Exception:
        pass
    return None

def score_priority(text: str, eta: Optional[date]):
    lowered = (text or "").lower()
    for p, kws in PRIORITY_KEYWORDS.items():
        for kw in kws:
            if kw in lowered:
                return p
    if eta:
        days = (eta - datetime.utcnow().date()).days
        if days <= 1:
            return "High"
        if days <= 5:
            return "Medium"
        return "Low"
    return "Medium"

def get_tasks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Task).order_by(models.Task.eta).offset(skip).limit(limit).all()

def get_tasks_by_date_range(db: Session, start: Optional[date], end: Optional[date]):
    q = db.query(models.Task)
    if start:
        q = q.filter(models.Task.eta >= start)
    if end:
        q = q.filter(models.Task.eta <= end)
    return q.order_by(models.Task.eta).all()

def create_task(db: Session, task: schemas.TaskCreate):
    db_task = models.Task(
        title=task.title,
        source=task.source,
        source_ref=task.source_ref,
        eta=task.eta,
        priority=task.priority or score_priority(task.title, task.eta),
        status=task.status or "Pending",
        extracted_from=task.extracted_from
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task

def detect_tasks_from_text(text: str):
    candidates = []
    if not text:
        return candidates
    sentences = [s.strip() for s in text.replace("\n", " ").split(".") if s.strip()]
    for s in sentences:
        lowered = s.lower()
        if any(k in lowered for k in ["please", "action", "complete", "update", "prepare", "send", "submit", "resolve"]):
            eta = parse_eta(s)
            candidates.append({"text": s, "eta": eta})
    return candidates

def extract_and_store(db: Session, emails=None, todos=None):
    added = []
    if todos:
        for t in todos:
            eta = None
            if getattr(t, "ETA_date", None):
                try:
                    eta = dateparser.parse(t.ETA_date).date()
                except Exception:
                    eta = None
            task = schemas.TaskCreate(
                title=t.task_title,
                source="todo",
                source_ref=None,
                eta=eta,
                extracted_from=t.task_title
            )
            db_task = create_task(db, task)
            added.append(db_task)
    if emails:
        for e in emails:
            found = detect_tasks_from_text(e.email_body)
            for tk in found:
                task = schemas.TaskCreate(
                    title=tk["text"],
                    source="email",
                    source_ref=e.subject,
                    eta=tk.get("eta"),
                    extracted_from=tk["text"]
                )
                db_task = create_task(db, task)
                added.append(db_task)
    return added
