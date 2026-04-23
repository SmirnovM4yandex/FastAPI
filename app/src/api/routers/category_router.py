from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.category_schema import CategorySchema
from src.dependencies.database import get_db
from src.domain.category_service import CategoryService
from src.api.exception_handler import handle_exception
from src.domain.auth_service import AuthService
from src.core.exceptions.exceptions import (
    NotFoundException,
    ConflictException,
    ValidationException
)

router = APIRouter(prefix="/categories", tags=["Categories"])


@router.get("/", response_model=List[CategorySchema])
async def get_categories(db: AsyncSession = Depends(get_db)):
    try:
        return await CategoryService(db).get_categories()
    except Exception as ex:
        handle_exception(ex)


@router.get("/{category_id}", response_model=CategorySchema)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    try:
        return await CategoryService(db).get_category(category_id)
    except Exception as ex:
        handle_exception(ex)


@router.post("/", response_model=CategorySchema, status_code=status.HTTP_201_CREATED)
async def create_category(
    data: CategorySchema,
    current_user = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await CategoryService(db).create_category(
            data.model_dump(),
            current_user
        )
    except ValidationException as exc:
        exc.log()
        raise HTTPException(status_code=400, detail=exc.message)
    except ConflictException as exc:
        exc.log()
        raise HTTPException(status_code=409, detail=exc.message)
    except Exception as ex:
        handle_exception(ex)


@router.put("/{category_id}", response_model=CategorySchema)
async def update_category(
    category_id: int,
    data: CategorySchema,
    current_user = Depends(AuthService.get_current_user),
    db: AsyncSession = Depends(get_db),
):
    try:
        return await CategoryService(db).update_category(
            category_id,
            data.model_dump(),
            current_user
        )
    except NotFoundException as exc:
        exc.log()
        raise HTTPException(status_code=404, detail=exc.message)
    except ConflictException as exc:
        exc.log()
        raise HTTPException(status_code=403, detail=exc.message)
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
    except NotFoundException as exc:
        exc.log()
        raise HTTPException(status_code=404, detail=exc.message)
    except ConflictException as exc:
        exc.log()
        raise HTTPException(status_code=403, detail=exc.message)
    except Exception as ex:
        handle_exception(ex)