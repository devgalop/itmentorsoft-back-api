from pydantic import BaseModel, field_validator
import re

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
            raise ValueError("Email is required")
        if len(value) < 5:
            raise ValueError("Email must be at least 5 characters long")
        if len(value) > 255:
            raise ValueError("Email must be no more than 255 characters long")
        if not re.match(EMAIL_PATTERN, value):
            raise ValueError("Invalid email format")
        return value

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        if not value:
            raise ValueError("Name is required")
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long")
        if len(value) > 100:
            raise ValueError("Name must be no more than 100 characters long")
        return value

    @field_validator("username")
    def validate_username(cls, value: str) -> str:
        if not value:
            raise ValueError("Username is required")
        if len(value) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(value) > 20:
            raise ValueError("Username must be no more than 20 characters long")
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
            raise ValueError("Role must be at least 3 characters long")
        if len(value) > 20:
            raise ValueError("Role must be no more than 20 characters long")
        return value
