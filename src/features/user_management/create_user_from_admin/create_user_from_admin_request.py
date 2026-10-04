from pydantic import BaseModel, field_validator
import re
from src.i18n import t

EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
USERNAME_PATTERN = r"\w+$"


class CreateUserFromAdminRequest(BaseModel):
    email: str
    name: str
    username: str
    role: str

    @field_validator("email")
    def validate_email(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.email.required"))
        if len(value) < 5:
            raise ValueError(t("validation.email.min_length"))
        if len(value) > 255:
            raise ValueError(t("validation.email.max_length"))
        if not re.match(EMAIL_PATTERN, value):
            raise ValueError(t("validation.email.format"))
        return value

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.name.required"))
        if len(value) < 3:
            raise ValueError(t("validation.name.min_length"))
        if len(value) > 100:
            raise ValueError(t("validation.name.max_length"))
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

    @field_validator("role")
    def validate_role(cls, value: str) -> str:
        if not value:
            raise ValueError("Role is required")
        if len(value) < 3:
            raise ValueError(t("validation.role.min_length"))
        if len(value) > 20:
            raise ValueError(t("validation.role.max_length"))
        return value
