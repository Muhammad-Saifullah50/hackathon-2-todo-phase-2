from datetime import datetime
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from sqlmodel import Session, select

from src.config import settings
from src.db.session import get_db
from src.models.user import User

ALGORITHM = "HS256"
ISSUER = "todo-auth"
AUDIENCE = "todo-api"

security = HTTPBearer()


class TokenData(BaseModel):
    """Payload data from the JWT token."""

    sub: str
    email: str | None = None
    name: str | None = None
    email_verified: bool = False


async def get_current_user(
    token: Annotated[HTTPAuthorizationCredentials, Depends(security)],
    session: Session = Depends(get_db),
) -> User:
    """
    Dependency to verify the JWT token and return the current user.

    Args:
        token: The Bearer token from the Authorization header.
        session: The database session.

    Returns:
        User: The authenticated user object.

    Raises:
        HTTPException: If the token is invalid, expired, or the user doesn't exist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token.credentials,
            settings.BETTER_AUTH_SECRET,
            algorithms=[ALGORITHM],
            audience=AUDIENCE,
            issuer=ISSUER,
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(
            sub=user_id,
            email=payload.get("email"),
            name=payload.get("name"),
            email_verified=payload.get("email_verified", False),
        )
    except JWTError:
        raise credentials_exception

    # Fetch user from database to ensure they still exist
    user = await session.get(User, token_data.sub)
    if user is None:
        raise credentials_exception

    return user
