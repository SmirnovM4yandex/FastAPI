from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class PostSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str
    text: str
    pub_date: datetime
    created_at: datetime
    author_id: int
    location_id: Optional[int] = None
    category_id: Optional[int] = None
    image: Optional[str] = None
    is_published: bool

    @field_validator("title")
    @classmethod
    def validate_title(cls, v):
        if not v or len(v.strip()) < 3:
            logger.error("Validation failed for post title: '%s'", v)
            raise ValueError("Title must be at least 3 characters")
        logger.info("Validated post title: %s", v)
        return v