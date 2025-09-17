from typing import Annotated

from core.dependencies.authentication import AuthenticationRequired
from core.session import get_session
from fastapi import Depends, HTTPException, status
from models.user import User
from sqlalchemy.orm import Session


def get_current_user(session: Annotated[Session, Depends(get_session)], auth: AuthenticationRequired = Depends()):
    user_id: int | None = auth.payload.get("sub")

    if not user_id:
        print("No user id")
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Unauthorized")

    user = session.get(User, user_id)

    if not user:
        print("No user")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

    return user
