from pydantic import BaseModel, field_validator
import re
from src.i18n import t

SPECIAL_CHAR_PATTERN = r'[!@#$%^&*()_+\-=\[\]{}|;\'":,.<>\/?]'


class ChangePasswordRequest(BaseModel):
    new_password: str

    @field_validator("new_password")
    def validate_password(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.password.required"))
        if len(value) < 6:
            raise ValueError(t("validation.password.min_length"))
        if len(value) > 20:
            raise ValueError(t("validation.password.max_length"))
        if not any(char.isdigit() for char in value):
            raise ValueError(t("validation.password.digit"))
        if not any(char.isalpha() for char in value):
            raise ValueError(t("validation.password.letter"))
        if not re.search(SPECIAL_CHAR_PATTERN, value):
            raise ValueError(t("validation.password.special"))
        return value


class ChangePasswordRequestWithToken(ChangePasswordRequest):
    token: str
    id_trx: str

    @field_validator("token")
    def validate_token(cls, value: str) -> str:
        if not value:
            raise ValueError("Token is required")
        if len(value) < 5:
            raise ValueError("Token must be at least 5 characters long")
        if len(value) > 255:
            raise ValueError("Token must be no more than 255 characters long")
        return value

    @field_validator("id_trx")
    def validate_id_trx(cls, value: str) -> str:
        if not value:
            raise ValueError("Transaction ID is required")
        if len(value) < 5:
            raise ValueError("Transaction ID must be at least 5 characters long")
        if len(value) > 255:
            raise ValueError("Transaction ID must be no more than 255 characters long")
        return value
