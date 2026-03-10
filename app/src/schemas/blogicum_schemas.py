from datetime import datetime
from pydantic import BaseModel, ConfigDict
from typing import Optional


class CategorySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    description: str
    slug: str


class LocationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str


class PostSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    text: str
    pub_date: datetime
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None


class CommentSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    post_id: int
    author_id: int
    text: str
