from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    Boolean,
    ForeignKey,
)

from src.database import Base
from src.core.settings import settings


class Post(Base):
    __tablename__ = "blog_post"

    id = Column(Integer, primary_key=True)

    title = Column(String(256), nullable=False)
    text = Column(Text, nullable=False)

    pub_date = Column(DateTime, nullable=True)

    author_id = Column(
        Integer,
        ForeignKey(
            f"{settings.POSTGRES_SCHEMA}.auth_user.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    location_id = Column(
        Integer,
        ForeignKey(f"{settings.POSTGRES_SCHEMA}.blog_location.id"),
        nullable=True
    )

    category_id = Column(
        Integer,
        ForeignKey(f"{settings.POSTGRES_SCHEMA}.blog_category.id"),
        nullable=True
    )

    image = Column(String, nullable=True)

    is_published = Column(Boolean, nullable=False, default=True)

    created_at = Column(DateTime, nullable=False)