from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.exception_handler import handle_exception
from src.core.exceptions.exceptions import (
    ConflictException,
    NotFoundException,
    ValidationException,
)
from src.dependencies.database import get_db
from src.domain.auth_service import AuthService
from src.domain.category_service import CategoryService
from src.schemas.category_schema import (
    CategoryCreateSchema,
    CategoryResponseSchema,
    CategoryUpdateSchema
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategoryResponseSchema])
async def get_categories(db: AsyncSession = Depends(get_db)):
    try:
        return await CategoryService(db).get_categories()
    except Exception as ex:
        handle_exception(ex)


@router.get("/{category_id}", response_model=CategoryResponseSchema)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await CategoryService(db).get_category(category_id)
    except Exception as ex:
        handle_exception(ex)


@router.post(
    "/",
    response_model=CategoryResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_category(
    data: CategoryCreateSchema,
    db: AsyncSession = Depends(get_db),
):
    try:
        return await CategoryService(db).create_category(
            data.model_dump()
        )

    except ValidationException as ex:
        ex.log()
        raise HTTPException(status_code=400, detail=ex.message)

    except ConflictException as ex:
        ex.log()
        raise HTTPException(status_code=409, detail=ex.message)

    except Exception as ex:
        handle_exception(ex)


@router.put("/{category_id}", response_model=CategoryResponseSchema)
async def update_category(
    category_id: int,
    data: CategoryUpdateSchema,
    current_user=Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await CategoryService(db).update_category(
            category_id,
            data.model_dump(exclude_unset=True),
            current_user,
        )

    except NotFoundException as ex:
        ex.log()
        raise HTTPException(status_code=404, detail=ex.message)

    except ConflictException as ex:
        ex.log()
        raise HTTPException(status_code=403, detail=ex.message)

    except Exception as ex:
        handle_exception(ex)

@router.delete("/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_category(
    category_id: int,
    current_user = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        await CategoryService(db).delete_category(category_id, current_user)
    except NotFoundException as ex:
        ex.log()
        raise HTTPException(status_code=404, detail=ex.message)
    except ConflictException as ex:
        ex.log()
        raise HTTPException(status_code=403, detail=ex.message)
    except Exception as ex:
        handle_exception(ex)