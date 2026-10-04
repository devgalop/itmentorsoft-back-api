from pydantic import BaseModel, field_validator
import re
from src.i18n import t

EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
SPECIAL_CHAR_PATTERN = r'[!@#$%^&*()_+\-=\[\]{}|;\'":,.<>\/?]'


class RecoveryPasswordRequest(BaseModel):
    email: str

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
