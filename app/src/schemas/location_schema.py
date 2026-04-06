from datetime import datetime
from pydantic import BaseModel, ConfigDict, field_validator
import logging

logger = logging.getLogger(__name__)

class LocationSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str
    is_published: bool
    created_at: datetime

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            logger.error("Validation failed for location name: empty value")
            raise ValueError("Location name cannot be empty")
        logger.info("Validated location name: %s", v)
        return v