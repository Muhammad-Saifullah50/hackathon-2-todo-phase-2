"""Integration tests for database connectivity."""

import pytest
from unittest.mock import patch, AsyncMock
from sqlalchemy import text
from sqlmodel.ext.asyncio.session import AsyncSession
from src.database import init_db, check_db_connection

@pytest.mark.asyncio
async def test_database_session_creation(test_session: AsyncSession) -> None:
    """Test that a database session can be created and used for a simple query."""
    result = await test_session.execute(text("SELECT 1"))
    assert result.scalar() == 1

@pytest.mark.asyncio
async def test_init_db(test_engine):
    """Test that init_db creates tables."""
    # This test relies on the test_engine fixture to create tables
    # so we just check if it runs without error.
    await init_db()

@pytest.mark.asyncio
@patch("src.database.engine")
async def test_check_db_connection_success(mock_engine: AsyncMock) -> None:
    """Test that check_db_connection returns True on success."""
    # Configure mock to return context manager that yields connection
    mock_conn = AsyncMock()
    mock_conn.execute.return_value = None
    mock_engine.connect.return_value.__aenter__.return_value = mock_conn
    
    assert await check_db_connection() is True

@pytest.mark.asyncio
@patch("src.database.engine")
async def test_check_db_connection_failure(mock_engine: AsyncMock) -> None:
    """Test that check_db_connection returns False on failure."""
    mock_engine.connect.side_effect = Exception("Connection failed")
    assert await check_db_connection() is False

@pytest.mark.asyncio
async def test_get_session_error_handling():
    """Test that get_session handles errors and rolls back."""
    from src.database import get_session, async_session_maker
    from unittest.mock import MagicMock
    
    with patch("src.database.async_session_maker") as mock_maker:
        mock_session = AsyncMock()
        mock_maker.return_value.__aenter__.return_value = mock_session
        
        # Simulate an error during session usage
        gen = get_session()
        await gen.__anext__() # Enter the try block
        
        try:
            # This is where the yield would be. We simulate an exception in the consumer.
            raise Exception("Session error")
        except Exception:
            with pytest.raises(Exception, match="Session error"):
                await gen.athrow(Exception("Session error"))
        
        # Verify rollback was called
        assert mock_session.rollback.called
        assert mock_session.close.called