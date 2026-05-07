from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey

from src.database import Base
from src.core.settings import settings


class Comment(Base):
    __tablename__ = "blog_comment"

    id = Column(Integer, primary_key=True)

    post_id = Column(
        Integer,
        ForeignKey(
            f"{settings.POSTGRES_SCHEMA}.blog_post.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    author_id = Column(
        Integer,
        ForeignKey(
            f"{settings.POSTGRES_SCHEMA}.auth_user.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    text = Column(Text, nullable=False)

    created_at = Column(DateTime, nullable=False)