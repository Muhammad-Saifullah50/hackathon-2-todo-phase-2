from datetime import datetime
from typing import TYPE_CHECKING
from uuid import UUID, uuid4

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .task import Task


class UserBase(SQLModel):
    """Base fields for User model, shared across schemas.

    Attributes:
        email: Unique email address for the user.
        name: Display name of the user (optional).
        image: URL to user's profile image (optional).
        email_verified: Timestamp when email was verified (optional).
    """

    email: str = Field(unique=True, index=True, description="User's email address")
    name: str | None = Field(default=None, description="User's full name")
    image: str | None = Field(default=None, description="URL to user's profile picture")
    email_verified: datetime | None = Field(
        default=None, description="Timestamp of email verification"
    )


class User(UserBase, table=True):
    """Database model for User entity.

    Attributes:
        id: Unique UUID identifier for the user.
        password_hash: Hashed password for authentication.
        created_at: Timestamp when account was created.
        updated_at: Timestamp when account was last updated.
        tasks: Relationship to tasks owned by this user.
    """

    __tablename__ = "users"

    id: UUID = Field(
        default_factory=uuid4, primary_key=True, description="Unique identifier for the user"
    )
    password_hash: str | None = Field(default=None, description="Bcrypt hashed password")
    created_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of account creation"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, description="Timestamp of last update"
    )

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user", cascade_delete=True)


class UserCreate(UserBase):
    """Schema for user registration.

    Attributes:
        password: Raw password provided during registration (hashed before storage).
    """

    password: str = Field(description="Raw password for account creation")


class UserResponse(UserBase):
    """Schema for user response payloads.

    Excludes sensitive fields like password_hash.
    """

    id: UUID
    created_at: datetime
    updated_at: datetime
