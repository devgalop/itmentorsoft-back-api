from pydantic import BaseModel, field_validator


class GetRecommendedContentRequest(BaseModel):
    student_id: str

    @field_validator("student_id")
    def validate_student_id(cls, value: str) -> str:
        if not value:
            raise ValueError("student_id must not be empty")
        if len(value) < 5:
            raise ValueError("student_id must be at least 5 characters long")
        if len(value) > 100:
            raise ValueError("student_id must not exceed 100 characters")
        return value
