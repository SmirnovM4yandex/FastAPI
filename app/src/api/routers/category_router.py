from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.category_schema import CategorySchema
from src.dependencies.database import get_db
from src.domain.category_service import CategoryService
from src.api.exception_handler import handle_exception

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategorySchema])
async def get_categories(db: AsyncSession = Depends(get_db)):
    try:
        return await CategoryService(db).get_categories()
    except Exception as ex:
        handle_exception(ex)


@router.get("/{category_id}", response_model=CategorySchema)
async def get_category(category_id: int,
                       db: AsyncSession = Depends(get_db)):
    try:
        return await CategoryService(db).get_category(category_id)
    except Exception as ex:
        handle_exception(ex)


@router.post("/", response_model=CategorySchema, status_code=201)
async def create_category(data: CategorySchema,
                          db: AsyncSession = Depends(get_db)):
    try:
        return await CategoryService(db).create_category(
            data.model_dump()
        )
    except Exception as ex:
        handle_exception(ex)


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(category_id: int,
                          data: CategorySchema,
                          db: AsyncSession = Depends(get_db)):
    try:
        return await CategoryService(db).update_category(
            category_id,
            data.model_dump()
        )
    except Exception as ex:
        handle_exception(ex)


@router.delete("/{category_id}", status_code=204)
async def delete_category(category_id: int,
                          db: AsyncSession = Depends(get_db)):
    try:
        await CategoryService(db).delete_category(category_id)
    except Exception as ex:
        handle_exception(ex)