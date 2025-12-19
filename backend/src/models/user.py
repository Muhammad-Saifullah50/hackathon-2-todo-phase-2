from datetime import datetime
from typing import TYPE_CHECKING

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from .task import Task


class UserBase(SQLModel):
    """Base fields for User model, shared across schemas.

    Attributes:
        email: Unique email address for the user.
        name: Display name of the user (optional).
        image: URL to user's profile image (optional).
    """

    email: str = Field(unique=True, index=True, description="User's email address")
    name: str | None = Field(default=None, description="User's full name")
    image: str | None = Field(default=None, description="URL to user's profile picture")


class User(UserBase, table=True):
    """Database model for User entity, managed by Better Auth.

    Attributes:
        id: Unique identifier for the user.
        emailVerified: Whether the email has been verified.
        createdAt: Timestamp when account was created.
        updatedAt: Timestamp when account was last updated.
        tasks: Relationship to tasks owned by this user.
    """

    __tablename__ = "user"
    __table_args__ = {"extend_existing": True}

    id: str = Field(primary_key=True, description="Unique identifier for the user")
    emailVerified: bool = Field(default=False, description="Whether the email is verified")
    createdAt: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updatedAt: datetime = Field(default_factory=datetime.utcnow, description="Update timestamp")

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user", cascade_delete=True)


class UserResponse(UserBase):
    """Schema for user response payloads.

    Excludes sensitive fields like passwords managed by Better Auth.
    """

    id: str
    emailVerified: bool
    createdAt: datetime
    updatedAt: datetime