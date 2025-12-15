from fastapi import APIRouter, Depends
from app.api.auth.deps import get_current_user
from app.api.users.schemas import UserMeResponse
from app.models.user import User

router = APIRouter(tags=["users"])

@router.get("/me", response_model=UserMeResponse)
def me(current_user: User = Depends(get_current_user)):
    return UserMeResponse(
        id=current_user.id,
        email=current_user.email,
        role=current_user.role,
        is_active=current_user.is_active,
    )
