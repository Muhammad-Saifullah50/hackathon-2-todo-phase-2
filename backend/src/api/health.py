"""Health check endpoints."""

from typing import Any

from fastapi import APIRouter, Response, status

from src.database import check_db_connection

router = APIRouter()


@router.get("")
async def health_check(response: Response) -> dict[str, Any]:
    """Basic health check endpoint.

    Returns:
        dict: Health status information including database connectivity

    Status Codes:
        200: Service is healthy and database is connected
        503: Service is degraded (database unreachable)
    """
    db_connected = await check_db_connection()

    # Set status code to 503 if database is unreachable
    if not db_connected:
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return {
        "status": "healthy" if db_connected else "degraded",
        "service": "todo-api",
        "version": "1.0.0",
        "database_connected": db_connected,
    }
