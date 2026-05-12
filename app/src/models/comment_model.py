from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey, func

from src.database import Base
from src.core.settings import settings


class Comment(Base):
    __tablename__ = "blog_comment"

    id = Column(Integer, primary_key=True)

    post_id = Column(
        Integer,
        ForeignKey(
            f"{settings.POSTGRES_SCHEMA}.blog_post.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    author_id = Column(
        Integer,
        ForeignKey(
            f"{settings.POSTGRES_SCHEMA}.auth_user.id",
            ondelete="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    text = Column(Text, nullable=False)

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )