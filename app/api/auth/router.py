from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import select

from app.api.deps import get_db
from app.api.auth.schemas import RegisterRequest, RegisterResponse, TokenResponse, LoginRequest
from app.core.security import get_password_hash
from app.models.user import User
from app.core.security import verify_password
from app.core.jwt import create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=RegisterResponse, status_code=status.HTTP_201_CREATED)
def register(payload: RegisterRequest, db: Session = Depends(get_db)):
    # check email exists
    stmt = select(User).where(User.email == payload.email)
    existing = db.execute(stmt).scalar_one_or_none()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered",
        )

    user = User(
        email=payload.email,
        hashed_password=get_password_hash(payload.password),
        role="user",
        is_active=True,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    return RegisterResponse(
        id=user.id,
        email=user.email,
        role=user.role,
        is_active=user.is_active,
    )

@router.post("/login", response_model=TokenResponse)
def login(payload: LoginRequest, db: Session = Depends(get_db)):
    stmt = select(User).where(User.email == payload.email)
    user = db.execute(stmt).scalar_one_or_none()

    if not user or not verify_password(payload.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )

    token = create_access_token(subject=user.email)
    return TokenResponse(access_token=token)
