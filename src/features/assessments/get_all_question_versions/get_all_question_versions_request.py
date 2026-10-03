from pydantic import BaseModel, field_validator
from src.i18n import t


class GetAllQuestionVersionsRequest(BaseModel):
    question_id: str

    @field_validator("question_id")
    def validate_question_id(cls, value: str) -> str:
        if not value:
            raise ValueError("question_id must not be empty")
        if len(value) < 3:
            raise ValueError("question_id must be at least 3 characters long")
        if len(value) > 100:
            raise ValueError(t("validation.question_id.max_length"))
        return value
