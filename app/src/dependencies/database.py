from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.database import session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with session() as db:
        yield db