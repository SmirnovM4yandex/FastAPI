from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.blogicum_schemas import CategorySchema
from src.repositories.category_repository import CategoryRepository
from src.dependencies.database import get_db


router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategorySchema])
async def get_categories(db: AsyncSession = Depends(get_db)):
    repo = CategoryRepository(db)
    return await repo.get_all()


@router.get("/{category_id}", response_model=CategorySchema)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    repo = CategoryRepository(db)

    category = await repo.get_by_id(category_id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


@router.post("/", response_model=CategorySchema, status_code=201)
async def create_category(data: CategorySchema, db:
                          AsyncSession = Depends(get_db)):
    repo = CategoryRepository(db)
    return await repo.create(data.model_dump())


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(category_id: int, data: CategorySchema, db:
                          AsyncSession = Depends(get_db)):
    repo = CategoryRepository(db)

    category = await repo.update(category_id, data.model_dump())
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")

    return category


@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int, db:
                          AsyncSession = Depends(get_db)):
    repo = CategoryRepository(db)

    success = await repo.delete(category_id)
    if not success:
        raise HTTPException(status_code=404, detail="Category not found")
