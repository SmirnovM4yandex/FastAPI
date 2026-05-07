from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.api.base import router as base_router
from src.api.routers.auth_router import router as auth_router
from src.core.settings import settings


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        root_path=settings.ROOT_PATH,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(base_router, prefix="/base")
    app.include_router(auth_router, tags=["Auth"])

    return app