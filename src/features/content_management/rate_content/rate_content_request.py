from pydantic import BaseModel, field_validator
from src.i18n import t


class RateContent(BaseModel):
    id: str
    content_id: str
    user_id: str
    rating: int
    comment: str | None = None


class RateContentRequest(BaseModel):
    content_id: str
    user_id: str
    rating: int
    comment: str | None = None

    @field_validator("content_id")
    def validate_content_id(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.content_id.required"))
        if len(value) > 100:
            raise ValueError(t("validation.content_id.max_length"))
        if len(value) < 10:
            raise ValueError(t("validation.content_id.min_length"))
        return value

    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.user_id.required"))
        if len(value) > 100:
            raise ValueError(t("validation.user_id.max_length"))
        if len(value) < 10:
            raise ValueError(t("validation.user_id.min_length_10"))
        return value

    @field_validator("rating")
    def validate_rating(cls, value: int) -> int:
        if value < 0 or value > 5:
            raise ValueError(t("validation.rating.range"))
        return value
