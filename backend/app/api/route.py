from fastapi import APIRouter

from .auth import auth_router
from .user import user_router

router = APIRouter()


router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
router.include_router(user_router, prefix="/user", tags=["User Management"])
