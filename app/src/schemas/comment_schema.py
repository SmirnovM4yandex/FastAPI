from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
import logging

logger = logging.getLogger(__name__)

class CommentSchema(BaseModel):
    """Класс комментария."""

    model_config = ConfigDict(from_attributes=True)
    post_id: int
    author_id: int
    text: str
    created_at: datetime

    @field_validator("text")
    @classmethod
    def validate_text(cls, v):
        if not v or len(v.strip()) == 0:
            logger.error("Validation failed for comment text: empty value")
            raise ValueError("Comment text cannot be empty")
        logger.info("Validated comment text")
        return v