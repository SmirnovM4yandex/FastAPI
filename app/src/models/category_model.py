from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean

from src.database import Base


class Category(Base):
    __tablename__ = "blog_category"

    id = Column(Integer, primary_key=True)

    title = Column(String(256), nullable=False)

    description = Column(Text, nullable=True)

    slug = Column(String(50), unique=True, nullable=False)

    is_published = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, nullable=False)