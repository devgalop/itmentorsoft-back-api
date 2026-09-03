from pydantic import BaseModel, field_validator

from src.features.assessments.shared.question_categories import QUESTION_CATEGORIES


class GetQuestionsByCategoryRequest(BaseModel):
    category: str

    @field_validator("category")
    def validate_category(cls, value: str) -> str:
        if not value:
            raise ValueError("Category cannot be empty")
        valid_values = list(QUESTION_CATEGORIES)
        if value not in valid_values:
            raise ValueError(
                f"Invalid category. Must be one of: {', '.join(valid_values)}"
            )
        return value
