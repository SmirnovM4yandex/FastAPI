from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .api.base import router as base_router
from .api.user import router as user_router
from .api.routers.auth_router import router as auth_router


def create_app() -> FastAPI:
    app = FastAPI(root_path="/api/v1")
    app.add_middleware(
        CORSMiddleware,  # type: ignore
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(base_router, prefix="/base")
    app.include_router(user_router, prefix="/user", tags=["User"])
    app.include_router(auth_router, tags=["Auth"])

    return app
