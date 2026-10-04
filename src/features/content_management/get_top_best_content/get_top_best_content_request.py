from pydantic import BaseModel, field_validator
from src.i18n import t


class GetTopBestContentRequest(BaseModel):
    topic: str
    limit: int = 10

    @field_validator("limit")
    def validate_limit(cls, value: int) -> int:
        if value < 1 or value > 50:
            raise ValueError(t("validation.limit.range"))
        return value

    @field_validator("topic")
    def validate_topic(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(t("validation.topic.required"))
        if len(value) < 3:
            raise ValueError(t("validation.topic.min_length"))
        if len(value) > 100:
            raise ValueError(t("validation.topic.max_length"))
        return value
