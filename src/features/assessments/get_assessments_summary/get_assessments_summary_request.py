from pydantic import BaseModel, field_validator


class GetAssessmentsSummaryRequest(BaseModel):
    student_id: str
    page: int = 0
    page_size: int = 10

    @field_validator("page", "page_size")
    def validate_positive(cls, value: int) -> int:
        if value < 0:
            raise ValueError("Value must be a non-negative integer.")
        return value

    @field_validator("page_size")
    def validate_page_size(cls, value: int) -> int:
        if value <= 0:
            raise ValueError("Page size must be a positive integer.")
        if value > 100:
            raise ValueError("Page size must not exceed 100.")
        return value

    @field_validator("student_id")
    def validate_student_id(cls, value: str) -> str:
        if not value:
            raise ValueError("Student ID must not be empty.")
        if len(value) < 5:
            raise ValueError("Student ID must be at least 5 characters long.")
        if len(value) > 100:
            raise ValueError("Student ID must be at most 100 characters long.")
        return value
