import re
from datetime import datetime
from enum import Enum
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from pydantic import field_validator
from sqlmodel import Field, Relationship, SQLModel

from .base import TimestampMixin

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
        due_date: Optional due date for task completion (with timezone).
        notes: Optional detailed notes in markdown format.
        manual_order: Optional user-defined sort order.
    """

    title: str = Field(index=True, description="Title or summary of the task")
    description: str | None = Field(default=None, description="Detailed description of the task")
    status: TaskStatus = Field(
        default=TaskStatus.PENDING, index=True, description="Current status of the task"
    )
    priority: TaskPriority = Field(
        default=TaskPriority.MEDIUM, index=True, description="Priority level of the task"
    )
    due_date: datetime | None = Field(
        default=None, description="Optional due date for task completion (UTC)"
    )
    notes: str | None = Field(default=None, description="Optional detailed notes (markdown)")
    manual_order: int | None = Field(default=None, description="User-defined sort order")
    template_id: UUID | None = Field(
        default=None, foreign_key="task_templates.id", description="Template used to create this task"
    )
    recurrence_pattern_id: UUID | None = Field(
        default=None,
        foreign_key="recurrence_patterns.id",
        description="Recurrence configuration for this task",
    )


class Task(TaskBase, TimestampMixin, table=True):
    """Database model for Task entity.

    Attributes:
        id: Unique UUID identifier for the task.
        user_id: Foreign key to the User who owns this task.
        created_at: Timestamp when task was created (from TimestampMixin).
        updated_at: Timestamp when task was last modified (from TimestampMixin).
        completed_at: Timestamp when task was marked as completed (optional).
        deleted_at: Timestamp when task was soft-deleted (optional, null for active tasks).
        user: Relationship to the parent User object.
    """

    __tablename__ = "tasks"

    id: UUID = Field(
        default_factory=uuid4, primary_key=True, description="Unique identifier for the task"
    )
    user_id: str = Field(
        foreign_key="user.id", index=True, description="ID of the user who owns this task"
    )
    completed_at: datetime | None = Field(
        default=None, description="Timestamp when task was completed"
    )
    deleted_at: datetime | None = Field(
        default=None, description="Timestamp when task was soft-deleted (null for active tasks)"
    )

    # Relationships
    user: "User" = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    """Schema for creating a new task.

    Inherits all fields from TaskBase with custom validation rules.

    Validation Rules:
        - Title: 1-100 characters AND 1-50 words (whitespace-trimmed, not empty)
        - Description: 0-500 characters (optional, whitespace-trimmed, empty→null)
        - Priority: LOW, MEDIUM, or HIGH (optional, defaults to MEDIUM)
        - Status: NOT accepted (always PENDING on creation)
    """

    @field_validator("title")
    @classmethod
    def validate_title(cls, v: str) -> str:
        """Validate title field with character and word count limits.

        Args:
            v: The title string to validate.

        Returns:
            Trimmed and validated title string.

        Raises:
            ValueError: If title is empty, exceeds 100 characters, or exceeds 50 words.
        """
        # Trim whitespace
        v = v.strip()

        # Check not empty
        if not v:
            raise ValueError("Title cannot be empty")

        # Check word count FIRST (50 words max, split by whitespace)
        # This is checked before character limit to match the spec requirement
        words = re.split(r"\s+", v)
        if len(words) > 50:
            raise ValueError("Title must be 50 words or less")

        # Check character limit (100 characters)
        if len(v) > 100:
            raise ValueError("Title must be 100 characters or less")

        return v

    @field_validator("description")
    @classmethod
    def validate_description(cls, v: str | None) -> str | None:
        """Validate description field with character limit.

        Args:
            v: The description string to validate (optional).

        Returns:
            Trimmed description string or None if empty.

        Raises:
            ValueError: If description exceeds 500 characters.
        """
        if v is None:
            return None

        # Trim whitespace
        v = v.strip()

        # Convert empty string to None
        if not v:
            return None

        # Check character limit (500 characters)
        if len(v) > 500:
            raise ValueError("Description must be 500 characters or less")

        return v


class TaskUpdate(SQLModel):
    """Schema for updating an existing task.

    All fields are optional to allow partial updates.
    """

    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None
    priority: TaskPriority | None = None


class TaskResponse(TaskBase):
    """Schema for task response payloads.

    Includes system-generated fields like id and timestamps.
    """

    id: UUID
    user_id: str
    created_at: datetime
    updated_at: datetime
    completed_at: datetime | None
    deleted_at: datetime | None