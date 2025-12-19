"""Main entry point for the Todo API application."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes import health
from src.config import settings

# Users and tasks routers will be added as they are implemented
# from src.api import users, tasks


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None]:
    """Lifespan events for the application.

    Handles startup and shutdown logic.
    """
    # Startup: Database connection check
    import logging

    from src.database import check_db_connection

    logger = logging.getLogger("uvicorn.error")

    if await check_db_connection():
        logger.info("Database connection verified successfully.")
    else:
        logger.error("Failed to connect to the database on startup.")

    yield
    # Shutdown: Clean up resources


app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="FastAPI backend for Todo application",
    lifespan=lifespan,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(health.router, prefix="/health", tags=["health"])
# app.include_router(users.router, prefix="/api/v1/users", tags=["users"])
# app.include_router(tasks.router, prefix="/api/v1/tasks", tags=["tasks"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("src.main:app", host="0.0.0.0", port=8000, reload=True)
