"""Health check endpoints."""

from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import text

from src.database import get_session

router = APIRouter()


@router.get("")
async def health_check() -> Dict[str, Any]:
    """Basic health check endpoint."""
    return {
        "status": "healthy",
        "service": "todo-api",
        "version": "1.0.0"
    }
