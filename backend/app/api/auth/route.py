from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security.jwt_handler import JWTHandler
from app.core.security.password_hasher import PasswordHasher
from app.core.session import get_session
from app.models.user import User
from app.schemas.auth import AuthResponse, LoginRequest, RegisterRequet

router = APIRouter()


def generate_token(user: User) -> AuthResponse:
    payload = {"first_name": user.first_name, "last_name": user.last_name, "email": user.email, "sub": str(user.id)}
    access_token: str = JWTHandler.encode(payload, "access")
    refresh_token: str = JWTHandler.encode(payload, "refresh")

    return AuthResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=AuthResponse)
async def register(request: RegisterRequet, session: Annotated[Session, Depends(get_session)]):
    stmt = select(User).where(User.email == request.email)
    existing = session.execute(stmt).scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    hashed_password = PasswordHasher.hash(request.password)

    user: User = User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password=hashed_password,
        phone_number=request.phone_number,
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return generate_token(user)


@router.post("/login", response_model=AuthResponse)
async def login(request: LoginRequest, session: Annotated[Session, Depends(get_session)]):
    stmt = select(User).where(User.email == request.email)
    user: User | None = session.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if not PasswordHasher.verify(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    return generate_token(user)
