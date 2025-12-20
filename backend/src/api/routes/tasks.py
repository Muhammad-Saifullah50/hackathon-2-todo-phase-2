"""API routes for task operations."""

import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import get_current_user
from src.db.session import get_db
from src.models.task import TaskCreate, TaskResponse
from src.models.user import User
from src.schemas.responses import StandardizedResponse
from src.services.task_service import TaskService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/v1/tasks", tags=["tasks"])


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=StandardizedResponse[TaskResponse],
)
async def create_task(
    task_data: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_db),
) -> StandardizedResponse[TaskResponse]:
    """Create a new task for the authenticated user.

    Args:
        task_data: Task creation data (title, description, priority).
        current_user: Authenticated user from JWT token.
        session: Database session.

    Returns:
        StandardizedResponse containing the created task.

    Raises:
        HTTPException: 400 for validation errors, 401 for auth errors, 500 for server errors.
    """
    try:
        # Initialize service
        service = TaskService(session)

        # Create task (user_id is extracted from JWT token)
        task = await service.create_task(task_data, current_user.id)

        # Log successful creation
        logger.info(f"Task created: id={task.id}, user_id={current_user.id}, title={task.title[:50]}")

        # Return success response
        return StandardizedResponse(
            success=True,
            message="Task created successfully",
            data=TaskResponse.model_validate(task),
        )

    except ValidationError as e:
        # Handle Pydantic validation errors
        logger.warning(f"Validation error creating task: {e}")
        errors = []
        for err in e.errors():
            errors.append({
                "field": ".".join(str(loc) for loc in err["loc"]),
                "message": err["msg"],
            })

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": "Invalid input data",
                },
                "details": errors,
            },
        )

    except ValueError as e:
        # Handle value errors (from validators)
        logger.warning(f"Value error creating task: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "error": {
                    "code": "VALIDATION_ERROR",
                    "message": str(e),
                },
            },
        )

    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Failed to create task: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error": {
                    "code": "INTERNAL_ERROR",
                    "message": "Failed to create task. Please try again later.",
                },
            },
        )
