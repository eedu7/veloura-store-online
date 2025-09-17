from typing import Annotated

from core.dependencies.authentication import AuthenticationRequired
from core.dependencies.get_current_user import get_current_user
from fastapi import APIRouter, Depends
from models.user import User
from schemas.user import UserOut

router = APIRouter(dependencies=[Depends(AuthenticationRequired)])


@router.get("/profile", response_model=UserOut)
async def profile(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
