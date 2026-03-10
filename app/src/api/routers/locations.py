from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from src.schemas.blogicum_schemas import LocationSchema
from src.repositories.location_repository import LocationRepository
from src.dependencies.database import get_db


router = APIRouter(prefix="/locations", tags=["Locations"])


@router.get("/", response_model=List[LocationSchema])
async def get_locations(db: AsyncSession = Depends(get_db)):
    repo = LocationRepository(db)
    return await repo.get_all()


@router.get("/{location_id}", response_model=LocationSchema)
async def get_location(location_id: int, db: AsyncSession = Depends(get_db)):
    repo = LocationRepository(db)

    location = await repo.get_by_id(location_id)
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return location


@router.post("/", response_model=LocationSchema, status_code=201)
async def create_location(data: LocationSchema, db:
                          AsyncSession = Depends(get_db)):
    repo = LocationRepository(db)
    return await repo.create(data.model_dump())


@router.put("/{location_id}", response_model=LocationSchema)
async def update_location(location_id: int, data: LocationSchema, db:
                          AsyncSession = Depends(get_db)):
    repo = LocationRepository(db)

    location = await repo.update(location_id, data.model_dump())
    if not location:
        raise HTTPException(status_code=404, detail="Location not found")

    return location


@router.delete("/{location_id}", status_code=204)
async def delete_location(location_id: int, db:
                          AsyncSession = Depends(get_db)):
    repo = LocationRepository(db)

    success = await repo.delete(location_id)
    if not success:
        raise HTTPException(status_code=404, detail="Location not found")
