from sqlalchemy import Column, Integer, String, DateTime, Boolean

from src.database import Base


class Location(Base):
    __tablename__ = "blog_location"

    id = Column(Integer, primary_key=True)

    name = Column(String(256), nullable=False)

    is_published = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, nullable=False)