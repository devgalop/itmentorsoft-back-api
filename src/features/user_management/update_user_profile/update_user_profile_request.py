import re
from pydantic import BaseModel, field_validator

USERNAME_PATTERN = r"\w+$"


class UpdateUserProfileRequest(BaseModel):
    user_id: str
    username: str
    name: str

    @field_validator("name")
    def validate_name(cls, value: str) -> str:
        if not value:
            raise ValueError("Name is required")
        if len(value) < 3:
            raise ValueError("Name must be at least 3 characters long")
        if len(value) > 100:
            raise ValueError("Name must be no more than 100 characters long")
        return value

    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError("User ID is required")
        if len(value) < 1:
            raise ValueError("User ID must be at least 1 character long")
        if len(value) > 100:
            raise ValueError("User ID must be no more than 100 characters long")
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
