from datetime import datetime
import logging

from pydantic import BaseModel, ConfigDict, field_validator

logger = logging.getLogger(__name__)


class LocationBaseSchema(BaseModel):
    name: str
    is_published: bool = True

    @field_validator("name")
    @classmethod
    def validate_name(cls, v):
        if not v or len(v.strip()) == 0:
            logger.error("Validation failed for location name")
            raise ValueError("Location name cannot be empty")
        return v


class LocationCreateSchema(LocationBaseSchema):
    pass


class LocationResponseSchema(LocationBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime