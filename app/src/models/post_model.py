from sqlalchemy import (Column, Integer, String, Text, DateTime,
                        Boolean, ForeignKey)

from src.database import Base


class Post(Base):
    __tablename__ = "blog_post"

    id = Column(Integer, primary_key=True)

    title = Column(String(256))
    text = Column(Text)
    pub_date = Column(DateTime)

    author_id = Column(Integer, ForeignKey("auth_user.id"))

    location_id = Column(Integer, ForeignKey("blog_location.id"),
                         nullable=True)
    category_id = Column(Integer, ForeignKey("blog_category.id"),
                         nullable=True)

    image = Column(String, nullable=True)

    is_published = Column(Boolean)
    created_at = Column(DateTime)
