from pydantic import BaseModel, field_validator
import re

EMAIL_PATTERN = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
SPECIAL_CHAR_PATTERN = r'[!@#$%^&*()_+\-=\[\]{}|;\'":,.<>\/?]'
GENERIC_ERROR_MESSAGE_LOGIN = "Invalid email or password"


class LoginRequest(BaseModel):
    email: str
    password: str

    @field_validator("email")
    def validate_email(cls, value: str) -> str:
        if not value:
            raise ValueError(GENERIC_ERROR_MESSAGE_LOGIN)
        if len(value) < 5:
            raise ValueError(GENERIC_ERROR_MESSAGE_LOGIN)
        if len(value) > 255:
            raise ValueError(GENERIC_ERROR_MESSAGE_LOGIN)
        if not re.match(EMAIL_PATTERN, value):
            raise ValueError(GENERIC_ERROR_MESSAGE_LOGIN)
        return value

    @field_validator("password")
    def validate_password(cls, value: str) -> str:
        if not value:
            raise ValueError(GENERIC_ERROR_MESSAGE_LOGIN)
        if len(value) < 6:
            raise ValueError(GENERIC_ERROR_MESSAGE_LOGIN)
        if len(value) > 20:
            raise ValueError(GENERIC_ERROR_MESSAGE_LOGIN)
        if not any(char.isdigit() for char in value):
            raise ValueError(GENERIC_ERROR_MESSAGE_LOGIN)
        if not any(char.isalpha() for char in value):
            raise ValueError(GENERIC_ERROR_MESSAGE_LOGIN)
        if not re.search(SPECIAL_CHAR_PATTERN, value):
            raise ValueError(GENERIC_ERROR_MESSAGE_LOGIN)
        return value
