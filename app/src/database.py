from contextlib import asynccontextmanager
from typing import AsyncIterator

from sqlalchemy import MetaData
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

from src.core.settings import settings


engine = create_async_engine(
    settings.postgres_url,
    echo=False,
)

AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False,
)


@asynccontextmanager
async def session() -> AsyncIterator[AsyncSession]:
    async with AsyncSessionLocal() as db:
        try:
            yield db
            await db.commit()
        except Exception:
            await db.rollback()
            raise


metadata = MetaData(schema=settings.POSTGRES_SCHEMA)


class Base(DeclarativeBase):
    metadata = metadata