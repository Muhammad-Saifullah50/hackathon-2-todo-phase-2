from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .user import User


class TaskStatus(str, Enum):
    """Enumeration for task completion status."""

    PENDING = "pending"
    COMPLETED = "completed"


class TaskPriority(str, Enum):
    """Enumeration for task priority levels."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class TaskBase(SQLModel):
    """Base fields for Task model, shared across creation and response schemas.

    Attributes:
        title: Summary of the task (required).
        description: Detailed information about the task (optional).
        status: Current completion status (default: pending).
        priority: Urgency level of the task (default: medium).
        due_date: Target date for task completion (optional).
    """

    title: str = Field(index=True, description="Title or summary of the task")
    description: str | None = Field(default=None, description="Detailed description of the task")
    status: TaskStatus = Field(
        default=TaskStatus.PENDING, index=True, description="Current status of the task"
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM, index=True, description="Priority level of the task"
    )
    due_date: datetime | None = Field(default=None, description="Target completion date")


class Task(TaskBase, table=True):
    """Database model for Task entity.

    Attributes:
        id: Unique UUID identifier for the task.
        user_id: Foreign key to the User who owns this task.
        created_at: Timestamp when task was created.
        updated_at: Timestamp when task was last modified.
        user: Relationship to the parent User object.
    """

    __tablename__ = "tasks"

    id: UUID = Field(
        default_factory=uuid4, primary_key=True, description="Unique identifier for the task"
    )
    user_id: UUID = Field(
        foreign_key="users.id", index=True, description="ID of the user who owns this task"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of task creation"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of last update"
    )

    # Relationships
    user: "User" = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """Schema for creating a new task.

    Inherits all fields from TaskBase.
    """

    pass


class TaskUpdate(SQLModel):
    """Schema for updating an existing task.

    All fields are optional to allow partial updates.
    """

    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None
    due_date: datetime | None = None


class TaskResponse(TaskBase):
    """Schema for task response payloads.

    Includes system-generated fields like id and timestamps.
    """

    id: UUID
    user_id: UUID
    created_at: datetime
    updated_at: datetime
