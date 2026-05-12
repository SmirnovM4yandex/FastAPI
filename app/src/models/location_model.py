from sqlalchemy import Column, Integer, String, DateTime, Boolean, func

from src.database import Base


class Location(Base):
    __tablename__ = "blog_location"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String(256), nullable=False, index=True)

    is_published = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)