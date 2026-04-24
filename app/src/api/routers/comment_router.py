from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.comment_schema import CommentSchema
from src.dependencies.database import get_db
from src.domain.comment_service import CommentService
from src.api.exception_handler import handle_exception
from src.domain.auth_service import AuthService

router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=List[CommentSchema])
async def get_comments(db: AsyncSession = Depends(get_db)):
    try:
        return await CommentService(db).get_comments()
    except Exception as ex:
        handle_exception(ex)


@router.get("/{comment_id}", response_model=CommentSchema)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await CommentService(db).get_comment(comment_id)
    except Exception as ex:
        handle_exception(ex)


@router.post("/", response_model=CommentSchema, status_code=status.HTTP_201_CREATED)
async def create_comment(
    data: CommentSchema,
    db: AsyncSession = Depends(get_db),
    current_user=Depends(AuthService.get_current_user),
):
    try:
        payload = data.model_dump()

        return await CommentService(db).create_comment(payload, current_user)
    except Exception as ex:
        handle_exception(ex)


@router.put("/{comment_id}", response_model=CommentSchema)
async def update_comment(
    comment_id: int,
    data: CommentSchema,
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
        await CommentService(db).delete_comment(comment_id, current_user=current_user)
    except Exception as ex:
        handle_exception(ex)
