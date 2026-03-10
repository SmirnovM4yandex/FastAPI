from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey

from src.database import Base


class Comment(Base):
    __tablename__ = "blog_comment"

    id = Column(Integer, primary_key=True)

    post_id = Column(Integer, ForeignKey("blog_post.id"))
    author_id = Column(Integer, ForeignKey("auth_user.id"))

    text = Column(Text)

    created_at = Column(DateTime)
