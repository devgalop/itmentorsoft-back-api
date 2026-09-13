from pydantic import BaseModel, field_validator


class ResendOtpRequest(BaseModel):
    user_id: str

    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError("User ID must not be empty.")
        if len(value) < 3:
            raise ValueError("User ID must be at least 3 characters long.")
        if len(value) > 100:
            raise ValueError("User ID must not exceed 100 characters.")
        return value
