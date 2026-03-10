from sqlalchemy import Column, Integer, String, DateTime, Boolean

from src.database import Base


class Location(Base):
    __tablename__ = "blog_location"

    id = Column(Integer, primary_key=True)
    name = Column(String(256))

    is_published = Column(Boolean)
    created_at = Column(DateTime)
