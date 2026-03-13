from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.blogicum_schemas import PostSchema
from src.dependencies.database import get_db
from src.domain.post_service import PostService


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostSchema])
async def get_posts(db: AsyncSession = Depends(get_db)):
    service = PostService(db)
    return await service.get_posts()


@router.get("/{post_id}", response_model=PostSchema)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    service = PostService(db)

    post = await service.get_post(post_id)

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.post("/", response_model=PostSchema, status_code=201)
async def create_post(data: PostSchema, db: AsyncSession = Depends(get_db)):
    service = PostService(db)
    return await service.create_post(data.model_dump())


@router.put("/{post_id}", response_model=PostSchema)
async def update_post(post_id: int, data: PostSchema, db:
                      AsyncSession = Depends(get_db)):
    service = PostService(db)

    post = await service.update_post(post_id, data.model_dump())

    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    service = PostService(db)

    success = await service.delete_post(post_id)

    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
