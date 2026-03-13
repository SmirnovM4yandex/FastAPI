from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.blogicum_schemas import CommentSchema
from src.dependencies.database import get_db
from src.domain.comment_service import CommentService


router = APIRouter(prefix="/comments", tags=["Comments"])


@router.get("/", response_model=List[CommentSchema])
async def get_comments(db: AsyncSession = Depends(get_db)):
    service = CommentService(db)
    return await service.get_comments()


@router.get("/{comment_id}", response_model=CommentSchema)
async def get_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    service = CommentService(db)

    comment = await service.get_comment(comment_id)

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment


@router.post("/", response_model=CommentSchema, status_code=201)
async def create_comment(data: CommentSchema, db:
                         AsyncSession = Depends(get_db)):
    service = CommentService(db)
    return await service.create_comment(data.model_dump())


@router.put("/{comment_id}", response_model=CommentSchema)
async def update_comment(comment_id: int, data: CommentSchema, db:
                         AsyncSession = Depends(get_db)):
    service = CommentService(db)

    comment = await service.update_comment(comment_id, data.model_dump())

    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    return comment


@router.delete("/{comment_id}", status_code=204)
async def delete_comment(comment_id: int, db: AsyncSession = Depends(get_db)):
    service = CommentService(db)

    success = await service.delete_comment(comment_id)

    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
