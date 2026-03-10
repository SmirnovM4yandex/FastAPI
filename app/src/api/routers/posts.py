from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.blogicum_schemas import PostSchema
from src.repositories.post_repository import PostRepository
from src.dependencies.database import get_db


router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostSchema])
async def get_posts(db: AsyncSession = Depends(get_db)):
    repo = PostRepository(db)
    return await repo.get_all()


@router.get("/{post_id}", response_model=PostSchema)
async def get_post(post_id: int, db: AsyncSession = Depends(get_db)):
    repo = PostRepository(db)

    post = await repo.get_by_id(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.post("/", response_model=PostSchema, status_code=201)
async def create_post(data: PostSchema, db: AsyncSession = Depends(get_db)):
    repo = PostRepository(db)
    return await repo.create(data.model_dump())


@router.put("/{post_id}", response_model=PostSchema)
async def update_post(post_id: int, data: PostSchema, db:
                      AsyncSession = Depends(get_db)):
    repo = PostRepository(db)

    post = await repo.update(post_id, data.model_dump())
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return post


@router.delete("/{post_id}", status_code=204)
async def delete_post(post_id: int, db: AsyncSession = Depends(get_db)):
    repo = PostRepository(db)

    success = await repo.delete(post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
