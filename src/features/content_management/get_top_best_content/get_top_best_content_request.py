from pydantic import BaseModel, field_validator


class GetTopBestContentRequest(BaseModel):
    topic: str
    limit: int = 10

    @field_validator("limit")
    def validate_limit(cls, value: int) -> int:
        if value < 1 or value > 50:
            raise ValueError("Limit must be between 1 and 50")
        return value

    @field_validator("topic")
    def validate_topic(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("Topic cannot be empty")
        if len(value) < 3:
            raise ValueError("Topic must be at least 3 characters long")
        if len(value) > 100:
            raise ValueError("Topic cannot exceed 100 characters")
        return value
