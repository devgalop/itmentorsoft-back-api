from pydantic import BaseModel, field_validator
from src.i18n import t


class UpdateQuestionStatusRequest(BaseModel):
    question_id: str
    status: bool

    @field_validator("question_id")
    def validate_question_id(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.question_id.required"))
        if len(value) < 5:
            raise ValueError(t("validation.question_id.min_length"))
        if len(value) > 100:
            raise ValueError(t("validation.question_id.max_length"))
        return value

    @field_validator("status")
    def validate_status(cls, value: bool) -> bool:
        if not isinstance(value, bool):
            raise ValueError(t("validation.status.boolean"))
        return value
