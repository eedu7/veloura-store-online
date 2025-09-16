from typing import Annotated

from core.session import get_session
from fastapi import APIRouter, Depends, HTTPException, status
from models.user import User
from schemas.auth import LoginRequest, RegisterRequet
from sqlalchemy import select
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(request: RegisterRequet, session: Annotated[Session, Depends(get_session)]):
    stmt = select(User).where(User.email == request.email)
    existing = session.execute(stmt).scalar_one_or_none()

    if existing:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User with this email already exists")

    user: User = User(
        first_name=request.first_name,
        last_name=request.last_name,
        email=request.email,
        password=request.password,
        phone_number=request.phone_number,
    )

    session.add(user)
    session.commit()
    session.refresh(user)
    return user


@router.post("/login")
async def login(request: LoginRequest, session: Annotated[Session, Depends(get_session)]):
    stmt = select(User).where(User.email == request.email)
    user: User | None = session.execute(stmt).scalar_one_or_none()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    if user.password != request.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")

    return {"message": "Login successful", "user": user}
