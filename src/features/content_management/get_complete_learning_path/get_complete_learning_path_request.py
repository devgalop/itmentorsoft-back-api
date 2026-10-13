from pydantic import BaseModel, field_validator


class GetCompleteLearningPathRequest(BaseModel):
    user_id: str
    page: int = 0
    page_size: int = 10

    @field_validator("page", "page_size")
    def non_negative(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Must be non-negative")
        return value

    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError("User ID must not be empty")
        if len(value) > 100:
            raise ValueError("User ID must not exceed 100 characters")
        if len(value) < 5:
            raise ValueError("User ID must be at least 5 characters")
        return value
