"""Task service for business logic operations."""

from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task, TaskCreate, TaskPriority, TaskStatus


class TaskService:
    """Service class for task-related business logic.

    This service layer separates business logic from the HTTP layer,
    making the code more testable and maintainable.

    Attributes:
        session: The async database session for database operations.
    """

    def __init__(self, session: AsyncSession):
        """Initialize the TaskService.

        Args:
            session: The async database session.
        """
        self.session = session

    async def create_task(self, task_data: TaskCreate, user_id: str) -> Task:
        """Create a new task for the authenticated user.

        Args:
            task_data: Validated task creation data from request.
            user_id: ID of the authenticated user from JWT token.

        Returns:
            Created Task instance with all fields populated.

        Raises:
            ValueError: If validation fails.
            SQLAlchemyError: If database operation fails.
        """
        # Create Task instance
        task = Task(
            title=task_data.title,  # Already validated and trimmed by Pydantic
            description=task_data.description,  # Already validated and trimmed
            status=TaskStatus.PENDING,  # Always pending on creation
            priority=task_data.priority or TaskPriority.MEDIUM,  # Default to MEDIUM
            user_id=user_id,
            # Timestamps are auto-set by TimestampMixin/database
        )

        # Add to session and commit
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task
