from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exception_handler import handle_exception
from src.dependencies.database import get_db
from src.domain.auth_service import AuthService
from src.domain.post_service import PostService
from src.schemas.post_schema import (
    PostCreateSchema,
    PostResponseSchema,
    PostUpdateSchema
)

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostResponseSchema])
async def get_posts(db: AsyncSession = Depends(get_db)):
    try:
        return await PostService(db).get_posts()
    except Exception as ex:
        handle_exception(ex)


@router.get("/{post_id}", response_model=PostResponseSchema)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await PostService(db).get_post(post_id)
    except Exception as ex:
        handle_exception(ex)


@router.post(
    "/",
    response_model=PostResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_post(
    data: PostCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(AuthService.get_current_user),
):
    try:
        return await PostService(db).create_post(
            data.model_dump(),
            current_user,
        )

    except Exception as ex:
        handle_exception(ex)


@router.put("/{post_id}", response_model=PostResponseSchema)
async def update_post(
    post_id: int,
    data: PostUpdateSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(AuthService.get_current_user),
):
    try:
        return await PostService(db).update_post(
            post_id,
            data.model_dump(),
            current_user=current_user,
        )

    except Exception as ex:
        handle_exception(ex)


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(
    post_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(AuthService.get_current_user),
):
    try:
        await PostService(db).delete_post(post_id, current_user=current_user)

    except Exception as ex:
        handle_exception(ex)
