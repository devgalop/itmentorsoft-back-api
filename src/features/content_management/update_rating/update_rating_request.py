from pydantic import BaseModel, field_validator


class UpdateRatingRequest(BaseModel):
    content_id: str
    user_id: str
    rating: int
    comment: str | None = None

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

    @field_validator("rating")
    def validate_rating(cls, value: int) -> int:
        if value < 0 or value > 5:
            raise ValueError("Rating must be between 0 and 5")
        return value
