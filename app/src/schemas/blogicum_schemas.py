from datetime import datetime
from pydantic import BaseModel
from typing import Optional


class CategorySchema(BaseModel):
    title: str
    description: str
    slug: str


class LocationSchema(BaseModel):
    name: str


class PostSchema(BaseModel):
    title: str
    text: str
    pub_date: datetime
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None


class CommentSchema(BaseModel):
    post_id: int
    author_id: int
    text: str
