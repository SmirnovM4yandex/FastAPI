from typing import List

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exception_handler import handle_exception
from src.dependencies.database import get_db
from src.domain.auth_service import AuthService
from src.domain.comment_service import CommentService
from src.schemas.comment_schema import (
    CommentCreateSchema,
    CommentResponseSchema,
)

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=List[CommentResponseSchema])
async def get_comments(db: AsyncSession = Depends(get_db)):
    try:
        return await CommentService(db).get_comments()
    except Exception as ex:
        handle_exception(ex)


@router.get("/{comment_id}", response_model=CommentResponseSchema)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await CommentService(db).get_comment(comment_id)
    except Exception as ex:
        handle_exception(ex)


@router.post(
    "/",
    response_model=CommentResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_comment(
    data: CommentCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(AuthService.get_current_user),
):
    try:
        return await CommentService(db).create_comment(
            data.model_dump(),
            current_user,
        )

    except Exception as ex:
        handle_exception(ex)


@router.put("/{comment_id}", response_model=CommentResponseSchema)
async def update_comment(
    comment_id: int,
    data: CommentCreateSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(AuthService.get_current_user),
):
    try:
        return await CommentService(db).update_comment(
            comment_id,
            data.model_dump(),
            current_user=current_user,
        )

    except Exception as ex:
        handle_exception(ex)


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_comment(
    comment_id: int,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(AuthService.get_current_user),
):
    try:
        await CommentService(db).delete_comment(
            comment_id,
            current_user=current_user,
        )

    except Exception as ex:
        handle_exception(ex)
