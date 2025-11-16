import os
import json
import re
from typing import List, Dict, Any
from datetime import datetime, timedelta
from dotenv import load_dotenv
from app.models import (
    ExtractedTask,
    OutlookEmail,
    LoopTask,
    TeamsMessage,
    SourceType,
    PriorityLevel,
    TaskStatus,
)

load_dotenv()


class AIEngine:
    def __init__(self):
        """Initialize AI Engine with Hugging Face models - FREE and NO API KEY needed!
        
        This uses lightweight models that don't require GPU or PyTorch GPU support.
        All processing is done locally - no data sent to any API!
        """
        print("Initializing Hugging Face AI Engine (completely free & local!)...")
        print("[OK] No API keys required")
        print("[OK] No premium subscriptions needed")
        print("[OK] All processing happens locally on your machine")
        
        # Try importing transformers with fallback
        try:
            from transformers import pipeline
            self.use_transformers = True
            print("[OK] Transformers library available")
            
            # Text generation pipeline
            try:
                self.generator = pipeline(
                    "text-generation",
                    model="distilgpt2",
                    device=-1  # CPU
                )
                print("[OK] Text generation model loaded")
            except:
                self.generator = None
                print("Note: Text generation model couldn't load")
            
            # Zero-shot classification
            try:
                self.classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli",
                    device=-1
                )
                print("[OK] Classification model loaded")
            except:
                self.classifier = None
                print("Note: Classification model couldn't load (will use keyword matching)")
                
        except ImportError:
            print("Transformers not fully available - using rule-based extraction")
            self.use_transformers = False
            self.generator = None
            self.classifier = None
        
        print("AI Engine ready!")
    
    def _extract_json_from_text(self, text: str) -> Dict[str, Any]:
        """Extract JSON from model output"""
        try:
            # Try to find JSON in the text
            json_match = re.search(r'\{.*\}', text, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                return json.loads(json_str)
        except:
            pass
        
        return {"tasks": []}

    def _classify_priority(self, text: str) -> str:
        """Classify text priority - first try model, then use keywords"""
        if self.classifier:
            try:
                result = self.classifier(
                    text[:512],
                    ["critical", "high", "medium", "low"],
                    multi_class=False
                )
                return result["labels"][0]
            except:
                pass
        
        # Keyword-based priority detection (always works!)
        text_lower = text.lower()
        
        critical_keywords = ["critical", "urgent", "asap", "emergency", "immediately", "!!!", "🔴", "top priority"]
        high_keywords = ["high", "important", "priority", "must", "!!", "🟠", "important", "should"]
        low_keywords = ["low", "maybe", "when possible", "eventually", "🟢", "optional"]
        
        if any(word in text_lower for word in critical_keywords):
            return "critical"
        elif any(word in text_lower for word in high_keywords):
            return "high"
        elif any(word in text_lower for word in low_keywords):
            return "low"
        
        return "medium"
    
    def _extract_tasks_rule_based(self, text: str, source_info: Dict[str, str]) -> List[Dict[str, Any]]:
        """Extract tasks using rule-based approach (always works, even without models)"""
        tasks = []
        
        # Simple rule: look for common patterns
        lines = text.split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or len(line) < 5:
                continue
            
            # Skip common non-task lines
            if any(skip in line.lower() for skip in ['from:', 'to:', 'subject:', 'sent:', 'date:', 'channel:', 'message:']):
                continue
            
            # Look for bullet points or numbers
            if line[0] in ['•', '◦', '-', '*', '1', '2', '3'] or ':' in line:
                task = {
                    "title": line.replace('•', '').replace('◦', '').replace('-', '').replace('*', '').strip()[:80],
                    "description": line[:200],
                    "priority": "medium",
                    "due_date": None,
                    "assigned_to": None
                }
                
                # Check priority keywords in this line
                task["priority"] = self._classify_priority(line)
                
                tasks.append(task)
        
        return tasks if tasks else [
            {
                "title": "Review " + source_info.get("source_type", "item"),
                "description": text[:100],
                "priority": "medium",
                "due_date": None,
                "assigned_to": None
            }
        ]

    def extract_tasks_from_email(self, email: OutlookEmail) -> List[ExtractedTask]:
        """Extract actionable tasks from email content (works with or without HF models)"""
        try:
            # Use rule-based extraction
            source_info = {"source_type": "email"}
            email_content = f"{email.subject}\n{email.body}"
            tasks_data = self._extract_tasks_rule_based(email_content, source_info)
            
            extracted_tasks = []
            for task_data in tasks_data:
                task = ExtractedTask(
                    title=task_data.get("title", "Untitled Task"),
                    description=task_data.get("description", ""),
                    source_type=SourceType.EMAIL,
                    source_id=email.id,
                    priority=PriorityLevel(task_data.get("priority", "medium")),
                    due_date=task_data.get("due_date"),
                    assigned_to=task_data.get("assigned_to"),
                    metadata={
                        "email_subject": email.subject,
                        "sender": email.sender_name,
                    },
                )
                extracted_tasks.append(task)
            
            return extracted_tasks

        except Exception as e:
            print(f"Error extracting tasks from email: {e}")
            return []

    def extract_tasks_from_teams(self, message: TeamsMessage) -> List[ExtractedTask]:
        """Extract actionable tasks from Teams/Slack messages (works with or without HF models)"""
        try:
            # Use rule-based extraction
            source_info = {"source_type": "teams"}
            teams_content = f"{message.channel}\n{message.sender_name}\n{message.message}"
            tasks_data = self._extract_tasks_rule_based(teams_content, source_info)
            
            extracted_tasks = []
            for task_data in tasks_data:
                task = ExtractedTask(
                    title=task_data.get("title", "Untitled Task"),
                    description=task_data.get("description", ""),
                    source_type=SourceType.TEAMS,
                    source_id=message.id,
                    priority=PriorityLevel(task_data.get("priority", "medium")),
                    due_date=task_data.get("due_date"),
                    assigned_to=task_data.get("assigned_to"),
                    metadata={
                        "channel": message.channel,
                        "sender": message.sender_name,
                        "mentions": message.mentions,
                    },
                )
                extracted_tasks.append(task)
            
            return extracted_tasks

        except Exception as e:
            print(f"Error extracting tasks from Teams message: {e}")
            return []

    def convert_loop_task(self, loop_task: LoopTask) -> ExtractedTask:
        """Convert Loop/To-Do task to extracted task format"""
        priority_mapping = {
            "high": PriorityLevel.HIGH,
            "medium": PriorityLevel.MEDIUM,
            "low": PriorityLevel.LOW,
        }

        status_mapping = {
            "pending": TaskStatus.PENDING,
            "in-progress": TaskStatus.IN_PROGRESS,
            "completed": TaskStatus.COMPLETED,
        }

        return ExtractedTask(
            title=loop_task.title,
            description=loop_task.description,
            source_type=SourceType.LOOP,
            source_id=loop_task.id,
            priority=priority_mapping.get(loop_task.priority, PriorityLevel.MEDIUM),
            due_date=datetime.fromisoformat(
                loop_task.due_date.replace("Z", "+00:00")
            ),
            assigned_to=loop_task.assigned_to,
            status=status_mapping.get(loop_task.status, TaskStatus.PENDING),
            metadata={"tags": loop_task.tags},
        )

    def prioritize_tasks(self, tasks: List[ExtractedTask]) -> List[ExtractedTask]:
        """Re-prioritize and rank tasks using Hugging Face models"""
        if not tasks:
            return []

        try:
            # Use classifier to re-evaluate priorities
            for task in tasks:
                combined_text = f"{task.title} {task.description}"
                priority = self._classify_priority(combined_text)
                task.priority = PriorityLevel(priority)
                task.metadata["priority_reasoning"] = f"Re-prioritized by HF classifier to {priority}"

            # Sort tasks by priority order with safe due date comparison
            priority_order = {
                PriorityLevel.CRITICAL: 0,
                PriorityLevel.HIGH: 1,
                PriorityLevel.MEDIUM: 2,
                PriorityLevel.LOW: 3,
            }
            
            def sort_key(t):
                # Primary sort by priority
                priority_val = priority_order.get(t.priority, 4)
                # Secondary sort by due date (handle None and timezone issues)
                try:
                    if t.due_date:
                        # Strip timezone for comparison
                        due_date_val = t.due_date.replace(tzinfo=None) if t.due_date.tzinfo else t.due_date
                        return (priority_val, due_date_val)
                except:
                    pass
                return (priority_val, datetime.max)
            
            tasks.sort(key=sort_key)
            return tasks

        except Exception as e:
            print(f"Error prioritizing tasks: {e}")
            return tasks

    def chat_interface(self, message: str, tasks_context: List[ExtractedTask]) -> str:
        """Handle chat interactions about tasks with intelligent analysis"""
        try:
            msg_lower = message.lower()
            
            # Smart task filtering based on query
            filtered_tasks = tasks_context
            
            # Helper function for safe datetime comparison
            def safe_compare_dates(task_date, compare_date):
                """Safely compare dates handling both naive and aware datetimes"""
                try:
                    if task_date.tzinfo:
                        task_date = task_date.replace(tzinfo=None)
                    return task_date, compare_date
                except:
                    return task_date, compare_date
            
            # Filter by time period
            if "today" in msg_lower:
                today = datetime.now().date()
                filtered_tasks = [t for t in filtered_tasks if t.due_date and t.due_date.date() == today]
            elif "tomorrow" in msg_lower:
                tomorrow = (datetime.now() + timedelta(days=1)).date()
                filtered_tasks = [t for t in filtered_tasks if t.due_date and t.due_date.date() == tomorrow]
            elif "week" in msg_lower:
                today = datetime.now().date()
                week_later = today + timedelta(days=7)
                filtered_tasks = [t for t in filtered_tasks if t.due_date and today <= t.due_date.date() <= week_later]
            elif "overdue" in msg_lower:
                now = datetime.now()
                safe_tasks = []
                for t in filtered_tasks:
                    if t.due_date:
                        try:
                            task_dt = t.due_date.replace(tzinfo=None) if t.due_date.tzinfo else t.due_date
                            if task_dt < now:
                                safe_tasks.append(t)
                        except:
                            pass
                filtered_tasks = safe_tasks
            
            # Filter by source
            if "email" in msg_lower and "@" not in msg_lower:
                filtered_tasks = [t for t in filtered_tasks if t.source_type == SourceType.EMAIL]
            elif "teams" in msg_lower:
                filtered_tasks = [t for t in filtered_tasks if t.source_type == SourceType.TEAMS]
            elif "loop" in msg_lower:
                filtered_tasks = [t for t in filtered_tasks if t.source_type == SourceType.LOOP]
            
            # Filter by status
            if "pending" in msg_lower or "incomplete" in msg_lower:
                filtered_tasks = [t for t in filtered_tasks if t.status == TaskStatus.PENDING]
            elif "completed" in msg_lower or "done" in msg_lower:
                filtered_tasks = [t for t in filtered_tasks if t.status == TaskStatus.COMPLETED]
            
            # Filter by priority
            if "critical" in msg_lower:
                filtered_tasks = [t for t in filtered_tasks if t.priority == PriorityLevel.CRITICAL]
            elif "high" in msg_lower and "priority" in msg_lower:
                filtered_tasks = [t for t in filtered_tasks if t.priority == PriorityLevel.HIGH]
            
            # Sort by priority and due date with safe datetime comparison
            priority_order = {
                PriorityLevel.CRITICAL: 0,
                PriorityLevel.HIGH: 1,
                PriorityLevel.MEDIUM: 2,
                PriorityLevel.LOW: 3,
            }
            
            def safe_sort_key(t):
                priority_val = priority_order.get(t.priority, 4)
                try:
                    if t.due_date:
                        # Strip timezone for safe comparison
                        due_date_val = t.due_date.replace(tzinfo=None) if t.due_date.tzinfo else t.due_date
                        return (priority_val, due_date_val)
                except:
                    pass
                return (priority_val, datetime.max)
            
            sorted_tasks = sorted(filtered_tasks, key=safe_sort_key)
            
            # Sophisticated response generation
            if not sorted_tasks:
                return "No tasks match your query. Would you like to see all tasks or ask something else?"
            
            if "how many" in msg_lower or "count" in msg_lower or "total" in msg_lower:
                total = len(sorted_tasks)
                critical_count = sum(1 for t in sorted_tasks if t.priority == PriorityLevel.CRITICAL)
                high_count = sum(1 for t in sorted_tasks if t.priority == PriorityLevel.HIGH)
                
                response = f"You have **{total} tasks** matching your criteria.\n"
                if critical_count > 0:
                    response += f"• {critical_count} critical (require immediate attention)\n"
                if high_count > 0:
                    response += f"• {high_count} high priority (should be done soon)\n"
                remaining = total - critical_count - high_count
                if remaining > 0:
                    response += f"• {remaining} medium/low priority (can be scheduled later)"
                return response.strip()
            
            elif "list" in msg_lower or "show" in msg_lower or "what are" in msg_lower or "get" in msg_lower:
                # Detailed task list with analysis
                response = f"**{len(sorted_tasks)} tasks** found:\n\n"
                for i, task in enumerate(sorted_tasks[:15], 1):
                    due_str = task.due_date.strftime("%b %d") if task.due_date else "No deadline"
                    priority_emoji = "🔴" if task.priority == PriorityLevel.CRITICAL else \
                                    "🟠" if task.priority == PriorityLevel.HIGH else \
                                    "🟡" if task.priority == PriorityLevel.MEDIUM else "🟢"
                    response += f"{priority_emoji} {i}. **{task.title}** ({due_str})\n"
                
                if len(sorted_tasks) > 15:
                    response += f"\n...and {len(sorted_tasks) - 15} more tasks"
                return response.strip()
            
            elif "priority" in msg_lower or "urgent" in msg_lower:
                # Focus on high-priority items
                critical = [t for t in sorted_tasks if t.priority == PriorityLevel.CRITICAL]
                high = [t for t in sorted_tasks if t.priority == PriorityLevel.HIGH]
                
                response = "**Priority Analysis:**\n\n"
                if critical:
                    response += f"🔴 **CRITICAL ({len(critical)} tasks)** - Act now!\n"
                    for t in critical[:3]:
                        response += f"  • {t.title}\n"
                    if len(critical) > 3:
                        response += f"  ... and {len(critical) - 3} more\n"
                
                if high:
                    response += f"\n🟠 **HIGH PRIORITY ({len(high)} tasks)** - Important\n"
                    for t in high[:3]:
                        response += f"  • {t.title}\n"
                    if len(high) > 3:
                        response += f"  ... and {len(high) - 3} more\n"
                
                if not critical and not high:
                    response += "No critical or high-priority tasks right now. Good job! 👍"
                
                return response.strip()
            
            elif "next" in msg_lower or "what should" in msg_lower or "recommend" in msg_lower:
                # Recommendation engine
                task = sorted_tasks[0]
                response = f"**Recommended Next Task:**\n\n"
                response += f"**{task.title}**\n"
                response += f"Priority: {task.priority.value.upper()}\n"
                if task.due_date:
                    response += f"Due: {task.due_date.strftime('%A, %B %d, %Y')}\n"
                response += f"Source: {task.source_type.value}\n"
                response += f"\n💡 Start with this task to maintain momentum!"
                return response.strip()
            
            elif "summary" in msg_lower or "overview" in msg_lower or "status" in msg_lower:
                # Executive summary
                all_tasks = tasks_context
                completed = sum(1 for t in all_tasks if t.status == TaskStatus.COMPLETED)
                pending = sum(1 for t in all_tasks if t.status == TaskStatus.PENDING)
                critical = sum(1 for t in all_tasks if t.priority == PriorityLevel.CRITICAL)
                
                # Safe datetime comparison - handle both naive and aware datetimes
                now = datetime.now()
                overdue = 0
                for t in all_tasks:
                    if t.due_date:
                        try:
                            # Compare naive datetimes
                            task_dt = t.due_date.replace(tzinfo=None) if t.due_date.tzinfo else t.due_date
                            if task_dt < now:
                                overdue += 1
                        except:
                            pass
                
                response = f"**📊 Task Summary:**\n\n"
                response += f"Total Tasks: {len(all_tasks)}\n"
                response += f"✅ Completed: {completed}\n"
                response += f"⏳ Pending: {pending}\n"
                response += f"🔴 Critical: {critical}\n"
                response += f"⚠️  Overdue: {overdue}\n"
                
                if overdue > 0:
                    response += f"\n⚠️  You have {overdue} overdue tasks! Prioritize these."
                else:
                    response += f"\n✨ You're on track! Keep up the good work."
                
                return response.strip()
            
            else:
                # Smart default response with insights
                critical = [t for t in sorted_tasks if t.priority == PriorityLevel.CRITICAL]
                high = [t for t in sorted_tasks if t.priority == PriorityLevel.HIGH]
                pending = [t for t in sorted_tasks if t.status == TaskStatus.PENDING]
                
                response = f"**📋 Current Status:**\n\n"
                
                if critical:
                    response += f"🔴 **Critical**: {len(critical)} tasks need immediate attention\n"
                    response += f"   → Start with: **{critical[0].title}**\n\n"
                elif high:
                    response += f"🟠 **High Priority**: {len(high)} important tasks\n"
                    response += f"   → Next: **{high[0].title}**\n\n"
                
                response += f"📊 You have {len(filtered_tasks)} tasks matching your criteria.\n"
                response += f"**What else would you like to know?**"
                
                return response.strip()

        except Exception as e:
            return f"I encountered an issue analyzing your tasks: {str(e)}"

    def generate_task_insights(self, tasks: List[ExtractedTask]) -> Dict[str, Any]:
        """Generate insights about the task list using calculated statistics"""
        if not tasks:
            return {"message": "No tasks to analyze"}

        try:
            # Calculate statistics
            critical_count = sum(1 for t in tasks if t.priority == PriorityLevel.CRITICAL)
            high_count = sum(1 for t in tasks if t.priority == PriorityLevel.HIGH)
            medium_count = sum(1 for t in tasks if t.priority == PriorityLevel.MEDIUM)
            low_count = sum(1 for t in tasks if t.priority == PriorityLevel.LOW)

            email_count = sum(1 for t in tasks if t.source_type == SourceType.EMAIL)
            teams_count = sum(1 for t in tasks if t.source_type == SourceType.TEAMS)
            loop_count = sum(1 for t in tasks if t.source_type == SourceType.LOOP)

            # Safe datetime comparison - handle both naive and aware datetimes
            now = datetime.now()
            overdue_count = 0
            upcoming = []
            
            for t in tasks:
                if t.due_date:
                    try:
                        # Compare naive datetimes
                        task_dt = t.due_date.replace(tzinfo=None) if t.due_date.tzinfo else t.due_date
                        if task_dt < now:
                            overdue_count += 1
                        # Check if upcoming (within next 3 days)
                        if now <= task_dt <= (now + timedelta(days=3)):
                            upcoming.append(t.title)
                    except:
                        pass

            insights = {
                "total_tasks": len(tasks),
                "by_priority": {
                    "critical": critical_count,
                    "high": high_count,
                    "medium": medium_count,
                    "low": low_count,
                },
                "by_source": {
                    "email": email_count,
                    "teams": teams_count,
                    "loop": loop_count,
                },
                "overdue_tasks": overdue_count,
                "upcoming_deadlines": upcoming,
                "key_insights": [
                    f"You have {critical_count} critical tasks that need immediate attention." if critical_count > 0 else "",
                    f"{email_count} tasks from emails, {teams_count} from Teams, {loop_count} from Loop.",
                    f"Total of {overdue_count} overdue tasks." if overdue_count > 0 else "",
                ],
                "recommendations": [
                    "Focus on critical and high-priority tasks first.",
                    "Review upcoming deadlines to plan your week effectively.",
                    "Consider breaking down large tasks into smaller subtasks.",
                ],
            }
            
            # Clean up empty insights
            insights["key_insights"] = [i for i in insights["key_insights"] if i]

            return insights

        except Exception as e:
            print(f"Error generating insights: {e}")
            return {"error": str(e)}
