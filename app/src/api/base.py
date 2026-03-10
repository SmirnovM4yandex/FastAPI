"""Маршрутизатор приложения."""
from fastapi import APIRouter

from .routers.posts import router as posts_router
from .routers.categories import router as categories_router
from .routers.locations import router as locations_router
from .routers.comments import router as comments_router


router = APIRouter()

router.include_router(posts_router)
router.include_router(categories_router)
router.include_router(locations_router)
router.include_router(comments_router)
