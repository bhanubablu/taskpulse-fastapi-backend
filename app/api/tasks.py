from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.task import Task, TaskStatus, TaskPriority
from app.schemas.task import TaskCreate, TaskUpdate, TaskResponse, TaskAnalyticsResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    task_in: TaskCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Create a new task assigned to current authenticated user."""
    task = Task(
        title=task_in.title,
        description=task_in.description,
        status=task_in.status.value if task_in.status else TaskStatus.PENDING.value,
        priority=task_in.priority.value if task_in.priority else TaskPriority.MEDIUM.value,
        due_date=task_in.due_date,
        owner_id=current_user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/", response_model=List[TaskResponse])
def list_tasks(
    status_filter: Optional[TaskStatus] = Query(None, alias="status"),
    priority_filter: Optional[TaskPriority] = Query(None, alias="priority"),
    search: Optional[str] = Query(None, description="Search keyword in title"),
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """List tasks owned by current user with optional filtering, search and pagination."""
    query = db.query(Task).filter(Task.owner_id == current_user.id)
    if status_filter:
        query = query.filter(Task.status == status_filter.value)
    if priority_filter:
        query = query.filter(Task.priority == priority_filter.value)
    if search:
        query = query.filter(Task.title.ilike(f"%{search}%"))

    return query.order_by(Task.created_at.desc()).offset(skip).limit(limit).all()

@router.get("/analytics/summary", response_model=TaskAnalyticsResponse)
def get_task_analytics(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Aggregate statistics for tasks owned by current user."""
    user_tasks = db.query(Task).filter(Task.owner_id == current_user.id).all()
    total = len(user_tasks)
    pending = sum(1 for t in user_tasks if t.status == TaskStatus.PENDING.value)
    in_progress = sum(1 for t in user_tasks if t.status == TaskStatus.IN_PROGRESS.value)
    completed = sum(1 for t in user_tasks if t.status == TaskStatus.COMPLETED.value)
    high_prio = sum(1 for t in user_tasks if t.priority in [TaskPriority.HIGH.value, TaskPriority.URGENT.value])
    
    rate = round((completed / total * 100), 2) if total > 0 else 0.0

    return {
        "total_tasks": total,
        "pending_tasks": pending,
        "in_progress_tasks": in_progress,
        "completed_tasks": completed,
        "completion_rate_percentage": rate,
        "high_priority_count": high_prio
    }

@router.get("/{task_id}", response_model=TaskResponse)
def get_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get a specific task by ID (ensures user owns the task)."""
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_in: TaskUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Update task fields (title, description, status, priority, due_date)."""
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    update_data = task_in.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            if hasattr(value, "value"):
                setattr(task, field, value.value)
            else:
                setattr(task, field, value)

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    task_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Delete a task owned by user."""
    task = db.query(Task).filter(Task.id == task_id, Task.owner_id == current_user.id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")

    db.delete(task)
    db.commit()
    return None
