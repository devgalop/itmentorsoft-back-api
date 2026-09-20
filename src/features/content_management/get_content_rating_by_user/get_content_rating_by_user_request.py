from pydantic import BaseModel, field_validator


class GetContentRatingByUserRequest(BaseModel):
    user_id: str
    content_id: str

    @field_validator("content_id")
    def validate_content_id(cls, value: str) -> str:
        if not value:
            raise ValueError("Content ID must not be empty")
        if len(value) > 100:
            raise ValueError("Content ID must not exceed 100 characters")
        if len(value) < 10:
            raise ValueError("Content ID must be at least 10 characters long")
        return value

    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError("User ID must not be empty")
        if len(value) > 100:
            raise ValueError("User ID must not exceed 100 characters")
        if len(value) < 10:
            raise ValueError("User ID must be at least 10 characters long")
        return value
