from typing import Annotated

from fastapi import APIRouter, Depends

from app.core.dependencies.authentication import AuthenticationRequired
from app.core.dependencies.get_current_user import get_current_user
from app.models.user import User
from app.schemas.user import UserOut

router = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.get("/profile", response_model=UserOut)
async def profile(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
