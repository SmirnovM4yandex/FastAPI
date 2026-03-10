from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.location_model import Location


class LocationRepository:

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self):
        result = await self.session.execute(select(Location))
        return result.scalars().all()

    async def get_by_id(self, location_id: int):
        result = await self.session.execute(
            select(Location).where(Location.id == location_id)
        )
        return result.scalar_one_or_none()

    async def create(self, data: dict):
        location = Location(**data)
        self.session.add(location)
        await self.session.commit()
        await self.session.refresh(location)
        return location
