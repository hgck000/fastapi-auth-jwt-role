from fastapi import Depends, HTTPException, status
from app.api.auth.deps import get_current_user
from app.models.user import User

def require_role(required_role: str):
    def _checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions",
            )
        return current_user
    return _checker
