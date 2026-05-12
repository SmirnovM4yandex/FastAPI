import logging

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.location_model import Location
from src.core.exceptions.exceptions import DatabaseException

logger = logging.getLogger(__name__)


class LocationRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self):
        try:
            result = await self.db.execute(
                select(Location).order_by(Location.id)
            )
            return result.scalars().all()

        except SQLAlchemyError as ex:
            logger.error("Failed to fetch locations: %s", ex)
            raise DatabaseException(str(ex))

    async def get_by_id(self, location_id: int):
        try:
            result = await self.db.execute(
                select(Location).where(Location.id == location_id)
            )
            return result.scalar_one_or_none()

        except SQLAlchemyError as ex:
            logger.error("Failed to fetch location id=%s: %s", location_id, ex)
            raise DatabaseException(str(ex))

    async def create(self, data: dict):
        try:
            location = Location(**data)

            self.db.add(location)

            await self.db.flush()
            await self.db.refresh(location)

            return location

        except SQLAlchemyError as ex:
            logger.error("Failed to create location: %s", ex)
            raise DatabaseException(str(ex))

    async def update(self, location_id: int, data: dict):
        try:
            location = await self.get_by_id(location_id)

            if not location:
                return None

            for key, value in data.items():
                if value is not None and hasattr(location, key):
                    setattr(location, key, value)

            await self.db.flush()
            await self.db.refresh(location)

            return location

        except SQLAlchemyError as ex:
            logger.error("Failed to update location id=%s: %s", location_id, ex)
            raise DatabaseException(str(ex))

    async def delete(self, location_id: int):
        try:
            location = await self.get_by_id(location_id)

            if not location:
                return False

            await self.db.delete(location)

            return True

        except SQLAlchemyError as ex:
            logger.error("Failed to delete location id=%s: %s", location_id, ex)
            raise DatabaseException(str(ex))