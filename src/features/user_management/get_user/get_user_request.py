from pydantic import BaseModel, field_validator
import re
from src.i18n import t

USERNAME_PATTERN = r"\w+$"


class GetUserRequest(BaseModel):
    user_id: str

    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.username.required"))
        if len(value) < 3:
            raise ValueError(t("validation.username.min_length"))
        if len(value) > 100:
            raise ValueError("Username must be no more than 100 characters long")
        if not re.match(USERNAME_PATTERN, value):
            raise ValueError(
                "Username must be alphanumeric and can include underscores"
            )
        return value
