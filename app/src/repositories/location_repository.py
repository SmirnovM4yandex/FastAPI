from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.location_model import Location


class LocationRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        result = await self.db.execute(select(Location))
        return result.scalars().all()

    async def get_by_id(self, location_id: int):
        result = await self.db.execute(
            select(Location).where(Location.id == location_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: dict):
        location = Location(**data)
        self.db.add(location)
        await self.db.commit()
        await self.db.refresh(location)
        return location

    async def update(self, location_id: int, data: dict):
        location = await self.get_by_id(location_id)

        if not location:
            return None

        for key, value in data.items():
            setattr(location, key, value)

        await self.db.commit()
        await self.db.refresh(location)

        return location

    async def delete(self, location_id: int):
        location = await self.get_by_id(location_id)

        if not location:
            return False

        await self.db.delete(location)
        await self.db.commit()

        return True
