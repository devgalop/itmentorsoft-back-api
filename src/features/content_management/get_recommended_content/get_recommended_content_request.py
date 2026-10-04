from pydantic import BaseModel, field_validator
from src.i18n import t


class GetRecommendedContentRequest(BaseModel):
    student_id: str

    @field_validator("student_id")
    def validate_student_id(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.student_id.required"))
        if len(value) < 5:
            raise ValueError(t("validation.student_id.min_length"))
        if len(value) > 100:
            raise ValueError(t("validation.student_id.max_length"))
        return value
