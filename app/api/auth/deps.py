from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.core.config import settings
from app.api.deps import get_db
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
) -> User:
    cred_exc = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALG])
        email: str | None = payload.get("sub")
        if not email:
            raise cred_exc
    except JWTError:
        raise cred_exc

    stmt = select(User).where(User.email == email)
    user = db.execute(stmt).scalar_one_or_none()
    if not user:
        raise cred_exc
    if not user.is_active:
        raise HTTPException(status_code=403, detail="Inactive user")

    return user
