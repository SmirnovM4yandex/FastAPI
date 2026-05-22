from sqlalchemy import (
    Column,
    Integer,
    ForeignKey,
    UniqueConstraint
)

from src.database import Base
from src.core.settings import settings


class PostReaction(Base):
    __tablename__ = "blog_post_reaction"

    id = Column(Integer, primary_key=True)

    post_id = Column(
        Integer,
        ForeignKey(
            f"{settings.POSTGRES_SCHEMA}.blog_post.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    user_id = Column(
        Integer,
        ForeignKey(
            f"{settings.POSTGRES_SCHEMA}.auth_user.id",
            ondelete="CASCADE"
        ),
        nullable=False
    )

    value = Column(Integer, nullable=False)

    __table_args__ = (
        UniqueConstraint(
            "post_id",
            "user_id",
            name="uq_post_user_reaction"
        ),
    )
