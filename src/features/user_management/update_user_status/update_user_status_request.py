from pydantic import BaseModel, field_validator
from src.i18n import t


class UpdateUserStatusRequest(BaseModel):
    user_id: str
    new_status: str

    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.user_id.required"))
        if len(value) < 5:
            raise ValueError(t("validation.user_id.min_length_5"))
        if len(value) > 100:
            raise ValueError(t("validation.user_id.max_length"))
        return value

    @field_validator("new_status")
    def validate_new_status(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.status.required"))
        if len(value) < 3:
            raise ValueError(t("validation.status.min_length"))
        if len(value) > 20:
            raise ValueError(t("validation.status.max_length"))
        return value
