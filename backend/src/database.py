import logging
from collections.abc import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.exc import DatabaseError, OperationalError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from .config import settings

logger = logging.getLogger(__name__)

# Create async engine with error handling
try:
    engine = create_async_engine(
        settings.DATABASE_URL,
        echo=settings.LOG_LEVEL == "DEBUG",
        future=True,
        pool_pre_ping=True,  # Verify connections before using them
    )
except Exception as e:
    logger.error(f"Failed to create database engine: {e}")
    raise

# Create session factory
async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    """Initialize database (create tables if they don't exist).
    Note: In production, we use Alembic for migrations.
    """
    try:
        async with engine.begin() as conn:
            # await conn.run_sync(SQLModel.metadata.drop_all)
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database tables initialized successfully")
    except OperationalError as e:
        logger.error(f"Database connection error during initialization: {e}")
        raise
    except DatabaseError as e:
        logger.error(f"Database error during initialization: {e}")
        raise
    except Exception as e:
        logger.error(f"Unexpected error during database initialization: {e}")
        raise


async def get_session() -> AsyncGenerator[AsyncSession]:
    """Dependency for obtaining a database session."""
    async with async_session_maker() as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Error during database session: {e}")
            await session.rollback()
            raise
        finally:
            await session.close()


async def check_db_connection() -> bool:
    """Check if the database connection is active.

    Returns:
        bool: True if connection is successful, False otherwise
    """
    try:
        async with engine.connect() as conn:
            await conn.execute(text("SELECT 1"))
        logger.info("Database connection check: SUCCESS")
        return True
    except OperationalError as e:
        logger.error(f"Database connection check FAILED (OperationalError): {e}")
        return False
    except DatabaseError as e:
        logger.error(f"Database connection check FAILED (DatabaseError): {e}")
        return False
    except Exception as e:
        logger.error(f"Database connection check FAILED (Unexpected error): {e}")
        return False
