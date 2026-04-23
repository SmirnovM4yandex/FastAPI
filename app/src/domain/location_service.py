from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.location_repository import LocationRepository
from src.core.exceptions.exceptions import (
    NotFoundException,
    ValidationException,
    ConflictException
)


class LocationService:

    def __init__(self, db: AsyncSession):
        self.repo = LocationRepository(db)

    async def get_locations(self):
        return await self.repo.get_all()

    async def get_location(self, location_id: int):
        location = await self.repo.get_by_id(location_id)

        if not location:
            raise NotFoundException("Location not found", {"location_id": location_id})

        return location

    async def create_location(self, data: dict, current_user):
        if not data["name"] or len(data["name"].strip()) == 0:
            raise ValidationException("Location name cannot be empty")

        return await self.repo.create(data)

    async def update_location(self, location_id: int, data: dict, current_user):
        if not current_user.is_superuser:
            raise ConflictException("Only superuser can update locations")

        location = await self.repo.update(location_id, data)

        if not location:
            raise NotFoundException("Location not found")

        return location

    async def delete_location(self, location_id: int, current_user):
        if not current_user.is_superuser:
            raise ConflictException("Only superuser can delete locations")

        success = await self.repo.delete(location_id)

        if not success:
            raise NotFoundException("Location not found")

        return True