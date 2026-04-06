from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.location_schema import LocationSchema
from src.domain.location_service import LocationService
from src.dependencies.database import get_db
from src.api.exception_handler import handle_exception

router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=List[LocationSchema])
async def get_locations(db: AsyncSession = Depends(get_db)):
    try:
        return await LocationService(db).get_locations()
    except Exception as ex:
        handle_exception(ex)


@router.get("/{location_id}", response_model=LocationSchema)
async def get_location(location_id: int,
                       db: AsyncSession = Depends(get_db)):
    try:
        return await LocationService(db).get_location(location_id)
    except Exception as ex:
        handle_exception(ex)


@router.post("/", response_model=LocationSchema, status_code=201)
async def create_location(data: LocationSchema,
                          db: AsyncSession = Depends(get_db)):
    try:
        return await LocationService(db).create_location(
            data.model_dump()
        )
    except Exception as ex:
        handle_exception(ex)


@router.put("/{location_id}", response_model=LocationSchema)
async def update_location(location_id: int,
                          data: LocationSchema,
                          db: AsyncSession = Depends(get_db)):
    try:
        return await LocationService(db).update_location(
            location_id,
            data.model_dump()
        )
    except Exception as ex:
        handle_exception(ex)


@router.delete("/{location_id}", status_code=204)
async def delete_location(location_id: int,
                          db: AsyncSession = Depends(get_db)):
    try:
        await LocationService(db).delete_location(location_id)
    except Exception as ex:
        handle_exception(ex)