import pytest
from jose import jwt
from fastapi import HTTPException
from src.auth import get_current_user, ALGORITHM, ISSUER, AUDIENCE
from src.config import settings
from src.models.user import User
from sqlalchemy.ext.asyncio import AsyncSession

@pytest.mark.asyncio
async def test_get_current_user_valid_token(test_session: AsyncSession):
    # Setup: Create a user in the test database
    user_id = "test-user-id"
    user = User(
        id=user_id,
        email="test@example.com",
        name="Test User",
    )
    test_session.add(user)
    await test_session.commit()

    # Generate a valid token
    payload = {
        "sub": user_id,
        "email": "test@example.com",
        "iss": ISSUER,
        "aud": AUDIENCE,
    }
    token = jwt.encode(payload, settings.BETTER_AUTH_SECRET, algorithm=ALGORITHM)

    # Mock the HTTPAuthorizationCredentials object
    class MockCreds:
        def __init__(self, token):
            self.credentials = token

    # Execute
    result = await get_current_user(MockCreds(token), test_session)

    # Verify
    assert result.id == user_id
    assert result.email == "test@example.com"

@pytest.mark.asyncio
async def test_get_current_user_invalid_token(test_session: AsyncSession):
    # Generate an invalid token (wrong secret)
    payload = {"sub": "id", "iss": ISSUER, "aud": AUDIENCE}
    token = jwt.encode(payload, "wrong-secret", algorithm=ALGORITHM)

    class MockCreds:
        def __init__(self, token):
            self.credentials = token

    # Execute & Verify
    with pytest.raises(HTTPException) as exc:
        await get_current_user(MockCreds(token), test_session)
    assert exc.value.status_code == 401
