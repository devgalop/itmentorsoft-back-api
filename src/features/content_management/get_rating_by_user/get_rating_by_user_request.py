from pydantic import BaseModel, field_validator
from src.i18n import t


class GetContentRatingByUserRequest(BaseModel):
    user_id: str

    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.user_id.required"))
        if len(value) > 100:
            raise ValueError(t("validation.user_id.max_length"))
        if len(value) < 10:
            raise ValueError(t("validation.user_id.min_length_10"))
        return value
