from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

from src.database import Base


class Category(Base):
    __tablename__ = "blog_category"

    id = Column(Integer, primary_key=True)
    title = Column(String(256))
    description = Column(Text)
    slug = Column(String(50), unique=True)

    is_published = Column(Boolean)
    created_at = Column(DateTime)
