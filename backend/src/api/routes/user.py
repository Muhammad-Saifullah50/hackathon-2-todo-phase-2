from fastapi import APIRouter, Depends
from src.auth import get_current_user
from src.models.user import User, UserResponse
from src.schemas.responses import StandardizedResponse

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=StandardizedResponse[UserResponse])
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current authenticated user profile.
    """
    return StandardizedResponse(
        data=UserResponse(
            id=current_user.id,
            email=current_user.email,
            name=current_user.name,
            image=current_user.image,
            emailVerified=current_user.emailVerified,
            createdAt=current_user.createdAt,
            updatedAt=current_user.updatedAt,
        )
    )
