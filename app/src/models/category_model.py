from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, func

from src.database import Base


class Category(Base):
    __tablename__ = "blog_category"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(256), nullable=False)
    description = Column(Text, nullable=True)

    slug = Column(String(50), unique=True, nullable=False, index=True)

    is_published = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)