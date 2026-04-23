"""Маршрутизатор приложения."""
from fastapi import APIRouter

from .routers.post_router import router as posts_router
from .routers.category_router import router as categories_router
from .routers.location_router import router as locations_router
from .routers.comment_router import router as comments_router
from .routers.user_router import router as users_router
from .routers.auth_router import router as auth_router


router = APIRouter()

router.include_router(posts_router)
router.include_router(categories_router)
router.include_router(locations_router)
router.include_router(comments_router)
router.include_router(users_router)
router.include_router(auth_router)
