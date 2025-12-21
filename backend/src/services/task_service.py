"""Task service for business logic operations."""

from datetime import datetime, timezone

from sqlalchemy import and_, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.task import Task, TaskCreate, TaskPriority, TaskStatus
from src.schemas.task_schemas import PaginationInfo, TaskListResponse, TaskMetadata


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
            due_date=task_data.due_date,  # Optional due date
            notes=task_data.notes,  # Optional notes
            user_id=user_id,
            # Timestamps are auto-set by TimestampMixin/database
        )

        # Add to session and commit
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def get_tasks(
        self,
        user_id: str,
        page: int = 1,
        limit: int = 20,
        status: TaskStatus | None = None,
        priority: TaskPriority | None = None,
        sort_by: str = "created_at",
        sort_order: str = "desc",
        search: str | None = None,
        due_date_from: datetime | None = None,
        due_date_to: datetime | None = None,
        has_due_date: bool | None = None,
    ) -> TaskListResponse:
        """Get paginated list of tasks with filtering and sorting.

        Args:
            user_id: ID of the authenticated user.
            page: Page number (1-indexed, default: 1).
            limit: Items per page (default: 20, max: 100).
            status: Filter by task status (optional).
            priority: Filter by task priority (optional).
            sort_by: Field to sort by (default: "created_at").
            sort_order: Sort direction "asc" or "desc" (default: "desc").
            search: Search in task title and description (optional).
            due_date_from: Filter tasks due after this date (optional).
            due_date_to: Filter tasks due before this date (optional).
            has_due_date: Filter tasks with/without due dates (optional).

        Returns:
            TaskListResponse with tasks, metadata, and pagination info.

        Raises:
            ValueError: If page/limit are invalid.
        """
        # Validate pagination parameters
        if page < 1:
            raise ValueError("Page must be >= 1")
        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")

        # Build base query with user filtering and soft delete exclusion
        filters = [
            Task.user_id == user_id,
            Task.deleted_at.is_(None),  # Exclude soft-deleted tasks
        ]

        # Add status filter if provided
        if status is not None:
            filters.append(Task.status == status)

        # Add priority filter if provided
        if priority is not None:
            filters.append(Task.priority == priority)

        # Add search filter if provided
        if search is not None and search.strip():
            search_term = f"%{search.strip()}%"
            filters.append(
                (Task.title.ilike(search_term)) | (Task.description.ilike(search_term))
            )

        # Add due date filters if provided
        if due_date_from is not None:
            filters.append(Task.due_date >= due_date_from)

        if due_date_to is not None:
            filters.append(Task.due_date <= due_date_to)

        # Add has_due_date filter if provided
        if has_due_date is not None:
            if has_due_date:
                filters.append(Task.due_date.isnot(None))
            else:
                filters.append(Task.due_date.is_(None))

        # Build count query for pagination
        count_query = select(func.count()).select_from(Task).where(and_(*filters))
        count_result = await self.session.execute(count_query)
        total_items = count_result.scalar_one()

        # Calculate pagination values
        total_pages = (total_items + limit - 1) // limit  # Ceiling division
        has_next = page < total_pages
        has_prev = page > 1

        # Build main query with sorting and pagination
        query = select(Task).where(and_(*filters))

        # Apply sorting
        sort_column = getattr(Task, sort_by, Task.created_at)
        if sort_order == "desc":
            query = query.order_by(sort_column.desc())
        else:
            query = query.order_by(sort_column.asc())

        # Apply pagination
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        # Execute query
        result = await self.session.execute(query)
        tasks = result.scalars().all()

        # Get metadata counts
        metadata = await self._get_task_metadata(user_id)

        # Build response
        pagination = PaginationInfo(
            page=page,
            limit=limit,
            total_items=total_items,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev,
        )

        return TaskListResponse(
            tasks=tasks,  # type: ignore
            metadata=metadata,
            pagination=pagination,
        )

    async def _get_task_metadata(self, user_id: str) -> TaskMetadata:
        """Get task count metadata for a user.

        Args:
            user_id: ID of the user.

        Returns:
            TaskMetadata with count statistics.
        """
        # Active tasks count
        active_query = (
            select(func.count())
            .select_from(Task)
            .where(and_(Task.user_id == user_id, Task.deleted_at.is_(None)))
        )
        active_result = await self.session.execute(active_query)
        total_active = active_result.scalar_one()

        # Pending tasks count
        pending_query = (
            select(func.count())
            .select_from(Task)
            .where(
                and_(
                    Task.user_id == user_id,
                    Task.deleted_at.is_(None),
                    Task.status == TaskStatus.PENDING,
                )
            )
        )
        pending_result = await self.session.execute(pending_query)
        total_pending = pending_result.scalar_one()

        # Completed tasks count
        completed_query = (
            select(func.count())
            .select_from(Task)
            .where(
                and_(
                    Task.user_id == user_id,
                    Task.deleted_at.is_(None),
                    Task.status == TaskStatus.COMPLETED,
                )
            )
        )
        completed_result = await self.session.execute(completed_query)
        total_completed = completed_result.scalar_one()

        # Deleted tasks count
        deleted_query = (
            select(func.count())
            .select_from(Task)
            .where(and_(Task.user_id == user_id, Task.deleted_at.isnot(None)))
        )
        deleted_result = await self.session.execute(deleted_query)
        total_deleted = deleted_result.scalar_one()

        return TaskMetadata(
            total_pending=total_pending,
            total_completed=total_completed,
            total_active=total_active,
            total_deleted=total_deleted,
        )

    async def update_task(
        self,
        task_id: str,
        user_id: str,
        title: str | None = None,
        description: str | None = None,
        due_date: datetime | None = None,
        notes: str | None = None,
        manual_order: int | None = None,
    ) -> Task:
        """Update a task's fields.

        Args:
            task_id: UUID of the task to update.
            user_id: ID of the authenticated user (for ownership verification).
            title: New title (optional).
            description: New description (optional).
            due_date: New due date (optional).
            notes: New notes (optional).
            manual_order: New manual order (optional).

        Returns:
            Updated Task instance.

        Raises:
            ValueError: If no fields to update, values unchanged, or task not found.
            PermissionError: If user doesn't own the task.
        """
        # Validate at least one field is provided
        if all(
            field is None
            for field in [title, description, due_date, notes, manual_order]
        ):
            raise ValueError("At least one field must be provided")

        # Fetch the task
        from uuid import UUID

        query = select(Task).where(
            and_(Task.id == UUID(task_id), Task.deleted_at.is_(None))
        )
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        # Verify ownership
        if task.user_id != user_id:
            raise PermissionError("You don't have permission to update this task")

        # Check if values are actually changing
        has_changes = False

        if title is not None and title != task.title:
            task.title = title
            has_changes = True

        if description is not None and description != task.description:
            task.description = description
            has_changes = True

        if due_date is not None and due_date != task.due_date:
            task.due_date = due_date
            has_changes = True

        if notes is not None and notes != task.notes:
            task.notes = notes
            has_changes = True

        if manual_order is not None and manual_order != task.manual_order:
            task.manual_order = manual_order
            has_changes = True

        if not has_changes:
            raise ValueError("No changes detected. Provided values are identical to current values")

        # Update updated_at timestamp (handled by trigger, but set explicitly for clarity)
        task.updated_at = datetime.now(timezone.utc)

        # Commit changes
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def toggle_task_status(self, task_id: str, user_id: str) -> Task:
        """Toggle a task's status between pending and completed.

        Args:
            task_id: UUID of the task to toggle.
            user_id: ID of the authenticated user (for ownership verification).

        Returns:
            Updated Task instance with new status.

        Raises:
            ValueError: If task not found.
            PermissionError: If user doesn't own the task.
        """
        from uuid import UUID

        # Fetch the task
        query = select(Task).where(
            and_(Task.id == UUID(task_id), Task.deleted_at.is_(None))
        )
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        # Verify ownership
        if task.user_id != user_id:
            raise PermissionError("You don't have permission to update this task")

        # Toggle status
        if task.status == TaskStatus.PENDING:
            task.status = TaskStatus.COMPLETED
            task.completed_at = datetime.now(timezone.utc)
        else:
            task.status = TaskStatus.PENDING
            task.completed_at = None

        # Update timestamp
        task.updated_at = datetime.now(timezone.utc)

        # Commit changes
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def bulk_toggle_status(
        self, task_ids: list[str], target_status: TaskStatus, user_id: str
    ) -> list[Task]:
        """Toggle multiple tasks to a target status atomically.

        Args:
            task_ids: List of task UUIDs to toggle (max 50).
            target_status: The status to set for all tasks.
            user_id: ID of the authenticated user (for ownership verification).

        Returns:
            List of updated Task instances.

        Raises:
            ValueError: If task_ids is empty, exceeds 50 tasks, or any task not found.
            PermissionError: If user doesn't own all tasks.
        """
        from uuid import UUID

        # Validate input
        if not task_ids:
            raise ValueError("task_ids cannot be empty")

        if len(task_ids) > 50:
            raise ValueError("Maximum 50 tasks per bulk operation")

        # Convert to UUIDs
        uuid_list = [UUID(task_id) for task_id in task_ids]

        # Fetch all tasks
        query = select(Task).where(
            and_(Task.id.in_(uuid_list), Task.deleted_at.is_(None))
        )
        result = await self.session.execute(query)
        tasks = list(result.scalars().all())

        # Verify all tasks found
        if len(tasks) != len(task_ids):
            raise ValueError(
                f"Found {len(tasks)} tasks but expected {len(task_ids)}. Some tasks may not exist."
            )

        # Verify ownership of all tasks
        for task in tasks:
            if task.user_id != user_id:
                raise PermissionError(
                    f"You don't have permission to update task {task.id}"
                )

        # Update all tasks
        now = datetime.now(timezone.utc)
        completed_at = now if target_status == TaskStatus.COMPLETED else None

        for task in tasks:
            task.status = target_status
            task.completed_at = completed_at
            task.updated_at = now
            self.session.add(task)

        # Commit all changes atomically
        await self.session.commit()

        # Refresh all tasks
        for task in tasks:
            await self.session.refresh(task)

        return tasks

    async def soft_delete_task(self, task_id: str, user_id: str) -> Task:
        """Soft delete a task by setting deleted_at timestamp.

        Args:
            task_id: UUID of the task to delete.
            user_id: ID of the authenticated user (for ownership verification).

        Returns:
            Soft-deleted Task instance with deleted_at timestamp.

        Raises:
            ValueError: If task not found.
            PermissionError: If user doesn't own the task.
        """
        from uuid import UUID

        # Fetch the task
        query = select(Task).where(
            and_(Task.id == UUID(task_id), Task.deleted_at.is_(None))
        )
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        # Verify ownership
        if task.user_id != user_id:
            raise PermissionError("You don't have permission to delete this task")

        # Set deleted_at timestamp
        task.deleted_at = datetime.now(timezone.utc)
        task.updated_at = datetime.now(timezone.utc)

        # Commit changes
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def bulk_delete_tasks(self, task_ids: list[str], user_id: str) -> list[Task]:
        """Soft delete multiple tasks atomically.

        Args:
            task_ids: List of task UUIDs to delete (max 50).
            user_id: ID of the authenticated user (for ownership verification).

        Returns:
            List of soft-deleted Task instances.

        Raises:
            ValueError: If task_ids is empty, exceeds 50 tasks, or any task not found.
            PermissionError: If user doesn't own all tasks.
        """
        from uuid import UUID

        # Validate input
        if not task_ids:
            raise ValueError("task_ids cannot be empty")

        if len(task_ids) > 50:
            raise ValueError("Maximum 50 tasks per bulk operation")

        # Convert to UUIDs
        uuid_list = [UUID(task_id) for task_id in task_ids]

        # Fetch all tasks
        query = select(Task).where(
            and_(Task.id.in_(uuid_list), Task.deleted_at.is_(None))
        )
        result = await self.session.execute(query)
        tasks = list(result.scalars().all())

        # Verify all tasks found
        if len(tasks) != len(task_ids):
            raise ValueError(
                f"Found {len(tasks)} tasks but expected {len(task_ids)}. Some tasks may not exist."
            )

        # Verify ownership of all tasks
        for task in tasks:
            if task.user_id != user_id:
                raise PermissionError(
                    f"You don't have permission to delete task {task.id}"
                )

        # Soft delete all tasks
        now = datetime.now(timezone.utc)

        for task in tasks:
            task.deleted_at = now
            task.updated_at = now
            self.session.add(task)

        # Commit all changes atomically
        await self.session.commit()

        # Refresh all tasks
        for task in tasks:
            await self.session.refresh(task)

        return tasks

    async def get_trash(
        self,
        user_id: str,
        page: int = 1,
        limit: int = 20,
    ) -> TaskListResponse:
        """Get paginated list of soft-deleted tasks (trash view).

        Args:
            user_id: ID of the authenticated user.
            page: Page number (1-indexed, default: 1).
            limit: Items per page (default: 20, max: 100).

        Returns:
            TaskListResponse with deleted tasks, metadata, and pagination info.

        Raises:
            ValueError: If page/limit are invalid.
        """
        # Validate pagination parameters
        if page < 1:
            raise ValueError("Page must be >= 1")
        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")

        # Build base query with user filtering and deleted tasks only
        filters = [
            Task.user_id == user_id,
            Task.deleted_at.isnot(None),  # Only show soft-deleted tasks
        ]

        # Build count query for pagination
        count_query = select(func.count()).select_from(Task).where(and_(*filters))
        count_result = await self.session.execute(count_query)
        total_items = count_result.scalar_one()

        # Calculate pagination values
        total_pages = (total_items + limit - 1) // limit  # Ceiling division
        has_next = page < total_pages
        has_prev = page > 1

        # Build main query with sorting and pagination
        query = select(Task).where(and_(*filters))

        # Sort by deleted_at (most recently deleted first)
        query = query.order_by(Task.deleted_at.desc())

        # Apply pagination
        offset = (page - 1) * limit
        query = query.offset(offset).limit(limit)

        # Execute query
        result = await self.session.execute(query)
        tasks = result.scalars().all()

        # Get metadata counts
        metadata = await self._get_task_metadata(user_id)

        # Build response
        pagination = PaginationInfo(
            page=page,
            limit=limit,
            total_items=total_items,
            total_pages=total_pages,
            has_next=has_next,
            has_prev=has_prev,
        )

        return TaskListResponse(
            tasks=tasks,  # type: ignore
            metadata=metadata,
            pagination=pagination,
        )

    async def restore_task(self, task_id: str, user_id: str) -> Task:
        """Restore a soft-deleted task by clearing deleted_at timestamp.

        Args:
            task_id: UUID of the task to restore.
            user_id: ID of the authenticated user (for ownership verification).

        Returns:
            Restored Task instance with deleted_at set to None.

        Raises:
            ValueError: If task not found or not in trash.
            PermissionError: If user doesn't own the task.
        """
        from uuid import UUID

        # Fetch the task from trash
        query = select(Task).where(
            and_(Task.id == UUID(task_id), Task.deleted_at.isnot(None))
        )
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise ValueError(f"Task with ID {task_id} not found in trash")

        # Verify ownership
        if task.user_id != user_id:
            raise PermissionError("You don't have permission to restore this task")

        # Clear deleted_at timestamp
        task.deleted_at = None
        task.updated_at = datetime.now(timezone.utc)

        # Commit changes
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def permanent_delete(self, task_id: str, user_id: str) -> None:
        """Permanently delete a task from the database (hard delete).

        Args:
            task_id: UUID of the task to permanently delete.
            user_id: ID of the authenticated user (for ownership verification).

        Raises:
            ValueError: If task not found or not in trash.
            PermissionError: If user doesn't own the task.
        """
        from uuid import UUID

        # Fetch the task from trash
        query = select(Task).where(
            and_(Task.id == UUID(task_id), Task.deleted_at.isnot(None))
        )
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise ValueError(f"Task with ID {task_id} not found in trash")

        # Verify ownership
        if task.user_id != user_id:
            raise PermissionError("You don't have permission to delete this task")

        # Hard delete from database
        await self.session.delete(task)
        await self.session.commit()

    async def get_tasks_by_due_date(
        self, user_id: str, filter: str | None = None, page: int = 1, limit: int = 20
    ) -> TaskListResponse:
        """Get tasks filtered by due date criteria with timezone handling.

        Args:
            user_id: ID of the user.
            filter: Due date filter (overdue/today/tomorrow/this_week/next_week/no_due_date).
            page: Page number (1-indexed).
            limit: Items per page (max 100).

        Returns:
            TaskListResponse with filtered tasks and pagination info.

        Raises:
            ValueError: If filter is invalid.
        """
        from datetime import timedelta

        # Validate pagination
        if page < 1:
            raise ValueError("Page must be >= 1")
        if limit < 1 or limit > 100:
            raise ValueError("Limit must be between 1 and 100")

        # Get current time in UTC
        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)

        # Base query: active tasks only
        base_query = select(Task).where(
            and_(Task.user_id == user_id, Task.deleted_at.is_(None))
        )

        # Apply due date filter
        if filter == "overdue":
            query = base_query.where(and_(Task.due_date.isnot(None), Task.due_date < today_start))
        elif filter == "today":
            query = base_query.where(and_(Task.due_date >= today_start, Task.due_date <= today_end))
        elif filter == "tomorrow":
            tomorrow_start = today_start + timedelta(days=1)
            tomorrow_end = today_end + timedelta(days=1)
            query = base_query.where(
                and_(Task.due_date >= tomorrow_start, Task.due_date <= tomorrow_end)
            )
        elif filter == "this_week":
            week_end = today_start + timedelta(days=7)
            query = base_query.where(and_(Task.due_date >= today_start, Task.due_date < week_end))
        elif filter == "next_week":
            week_start = today_start + timedelta(days=7)
            week_end = week_start + timedelta(days=7)
            query = base_query.where(and_(Task.due_date >= week_start, Task.due_date < week_end))
        elif filter == "no_due_date":
            query = base_query.where(Task.due_date.is_(None))
        elif filter is None:
            query = base_query  # No filter, return all active tasks
        else:
            raise ValueError(
                f"Invalid filter: {filter}. "
                "Valid options: overdue, today, tomorrow, this_week, next_week, no_due_date"
            )

        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_count_result = await self.session.execute(count_query)
        total_count = total_count_result.scalar_one()

        # Apply pagination
        offset = (page - 1) * limit
        query = query.order_by(Task.due_date.asc().nullslast(), Task.created_at.desc())
        query = query.offset(offset).limit(limit)

        # Execute query
        result = await self.session.execute(query)
        tasks = result.scalars().all()

        # Calculate pagination info
        total_pages = (total_count + limit - 1) // limit if total_count > 0 else 0

        # Get metadata
        metadata = await self._get_task_metadata(user_id)

        return TaskListResponse(
            tasks=[task for task in tasks],
            metadata=metadata,
            pagination=PaginationInfo(
                page=page,
                limit=limit,
                total_items=total_count,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_prev=page > 1,
            ),
        )

    async def update_task_due_date(
        self, task_id: str, user_id: str, due_date: datetime | None
    ) -> Task:
        """Update or remove a task's due date.

        Args:
            task_id: UUID of the task.
            user_id: ID of the user (for permission check).
            due_date: New due date (with timezone) or None to remove.

        Returns:
            Updated Task object.

        Raises:
            ValueError: If task not found.
            PermissionError: If user doesn't own the task.
        """
        from uuid import UUID

        # Fetch task
        query = select(Task).where(
            and_(Task.id == UUID(task_id), Task.deleted_at.is_(None))
        )
        result = await self.session.execute(query)
        task = result.scalar_one_or_none()

        if not task:
            raise ValueError(f"Task with ID {task_id} not found")

        # Verify ownership
        if task.user_id != user_id:
            raise PermissionError("You don't have permission to update this task")

        # Update due date
        task.due_date = due_date
        task.updated_at = datetime.now(timezone.utc)

        await self.session.commit()
        await self.session.refresh(task)

        return task

    async def get_due_date_stats(self, user_id: str) -> dict:
        """Get statistics for tasks by due date categories.

        Args:
            user_id: ID of the user.

        Returns:
            Dictionary with counts for overdue, due today, due this week, no due date.
        """
        from datetime import timedelta
        from src.schemas.task_schemas import DueDateStatsResponse

        now = datetime.now(timezone.utc)
        today_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        today_end = now.replace(hour=23, minute=59, second=59, microsecond=999999)
        week_end = today_start + timedelta(days=7)

        # Base query: active tasks only
        base_query = select(func.count()).where(
            and_(Task.user_id == user_id, Task.deleted_at.is_(None))
        )

        # Overdue count
        overdue_query = base_query.where(and_(Task.due_date.isnot(None), Task.due_date < today_start))
        overdue_result = await self.session.execute(overdue_query)
        overdue_count = overdue_result.scalar_one()

        # Due today count
        today_query = base_query.where(and_(Task.due_date >= today_start, Task.due_date <= today_end))
        today_result = await self.session.execute(today_query)
        due_today_count = today_result.scalar_one()

        # Due this week count
        week_query = base_query.where(and_(Task.due_date >= today_start, Task.due_date < week_end))
        week_result = await self.session.execute(week_query)
        due_this_week_count = week_result.scalar_one()

        # No due date count
        no_due_query = base_query.where(Task.due_date.is_(None))
        no_due_result = await self.session.execute(no_due_query)
        no_due_date_count = no_due_result.scalar_one()

        return DueDateStatsResponse(
            overdue_count=overdue_count,
            due_today_count=due_today_count,
            due_this_week_count=due_this_week_count,
            no_due_date_count=no_due_date_count,
        )
