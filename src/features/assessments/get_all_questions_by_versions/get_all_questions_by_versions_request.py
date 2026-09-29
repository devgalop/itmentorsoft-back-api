from pydantic import BaseModel, field_validator


class GetAllQuestionsByVersionsRequest(BaseModel):
    page: int = 0
    page_size: int = 10

    @field_validator("page")
    def validate_page(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Page must be a non-negative integer")
        return value

    @field_validator("page_size")
    def validate_page_size(cls, value: int) -> int:
        if value < 1:
            raise ValueError("Page size must be at least 1")
        if value > 100:
            raise ValueError("Page size must not exceed 100")
        return value
