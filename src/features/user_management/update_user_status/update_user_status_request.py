from pydantic import BaseModel, field_validator


class UpdateUserStatusRequest(BaseModel):
    user_id: str
    new_status: str

    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError("User ID must not be empty")
        if len(value) < 5:
            raise ValueError("User ID must be at least 5 characters long")
        if len(value) > 100:
            raise ValueError("User ID must be no more than 100 characters long")
        return value

    @field_validator("new_status")
    def validate_new_status(cls, value: str) -> str:
        if not value:
            raise ValueError("New status must not be empty")
        if len(value) < 3:
            raise ValueError("New status must be at least 3 characters long")
        if len(value) > 20:
            raise ValueError("New status must be no more than 20 characters long")
        return value
