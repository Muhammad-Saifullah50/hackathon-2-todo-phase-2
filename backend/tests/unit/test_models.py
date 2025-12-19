from uuid import UUID

from src.models.task import Task, TaskPriority, TaskStatus
from src.models.user import User


def test_user_model_creation() -> None:
    """Test creating a User model instance."""
    user = User(email="test@example.com", name="Test User")
    assert isinstance(user.id, UUID)
    assert user.email == "test@example.com"
    assert user.name == "Test User"
    assert user.password_hash is None


def test_task_model_creation() -> None:
    """Test creating a Task model instance."""
    user_id = UUID("550e8400-e29b-41d4-a716-446655440000")
    task = Task(
        title="Test Task",
        description="Test Description",
        user_id=user_id,
        status=TaskStatus.PENDING,
        priority=TaskPriority.HIGH,
    )
    assert isinstance(task.id, UUID)
    assert task.title == "Test Task"
    assert task.user_id == user_id
    assert task.status == TaskStatus.PENDING
    assert task.priority == TaskPriority.HIGH
