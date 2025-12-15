from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_db
from app.api.auth.roles import require_role
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])

@router.get("/users")
def list_users(
    db: Session = Depends(get_db),
    _admin: User = Depends(require_role("admin")),
):
    users = db.execute(select(User).order_by(User.id)).scalars().all()
    return [
        {
            "id": u.id,
            "email": u.email,
            "role": u.role,
            "is_active": u.is_active,
        }
        for u in users
    ]
