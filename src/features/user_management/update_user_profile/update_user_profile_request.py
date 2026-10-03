import re
from pydantic import BaseModel, field_validator
from src.i18n import t

USERNAME_PATTERN = r"\w+$"


class UpdateUserProfileRequest(BaseModel):
    user_id: str
    username: str
    name: str

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.name.required"))
        if len(value) < 3:
            raise ValueError(t("validation.name.min_length"))
        if len(value) > 100:
            raise ValueError(t("validation.name.max_length"))
        return value

    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError("User ID is required")
        if len(value) < 1:
            raise ValueError(t("validation.user_id.min_length_1"))
        if len(value) > 100:
            raise ValueError(t("validation.user_id.max_length"))
        return value

    @field_validator("username")
    def validate_username(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.username.required"))
        if len(value) < 3:
            raise ValueError(t("validation.username.min_length"))
        if len(value) > 20:
            raise ValueError(t("validation.username.max_length"))
        if not re.match(USERNAME_PATTERN, value):
            raise ValueError(
                "Username must be alphanumeric and can include underscores"
            )
        return value
