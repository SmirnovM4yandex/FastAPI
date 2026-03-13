from sqlalchemy.ext.asyncio import AsyncSession
from src.repositories.location_repository import LocationRepository


class LocationService:

    def __init__(self, db: AsyncSession):
        self.repo = LocationRepository(db)

    async def get_locations(self):
        return await self.repo.get_all()

    async def get_location(self, location_id: int):
        return await self.repo.get_by_id(location_id)

    async def create_location(self, data: dict):
        return await self.repo.create(data)

    async def update_location(self, location_id: int, data: dict):
        return await self.repo.update(location_id, data)

    async def delete_location(self, location_id: int):
        return await self.repo.delete(location_id)
