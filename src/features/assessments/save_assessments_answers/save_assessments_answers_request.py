from pydantic import BaseModel, field_validator
from src.i18n import t


class AssessmentAnswer(BaseModel):
    question_id: str
    answer: str
    takes_time_seconds: int

    @field_validator("question_id")
    def validate_question_id(cls, value: str) -> str:
        if not value:
            raise ValueError("question_id must not be empty")
        if len(value) > 200:
            raise ValueError("question_id must not exceed 200 characters")
        if len(value) < 5:
            raise ValueError(t("validation.question_id.min_length"))
        return value

    @field_validator("answer")
    def validate_answer(cls, value: str) -> str:
        if not value:
            raise ValueError("answer must not be empty")
        if len(value) > 600:
            raise ValueError("answer must not exceed 600 characters")
        return value

    @field_validator("takes_time_seconds")
    def validate_takes_time_seconds(cls, value: int) -> int:
        if value < 0:
            raise ValueError("takes_time_seconds must be a non-negative integer")
        return value


class SaveAssessmentsAnswersRequest(BaseModel):
    assessment_id: str
    user_id: str
    answers: list[AssessmentAnswer]

    @field_validator("assessment_id")
    def validate_assessment_id(cls, value: str) -> str:
        if not value:
            raise ValueError("assessment_id must not be empty")
        if len(value) > 200:
            raise ValueError("assessment_id must not exceed 200 characters")
        if len(value) < 5:
            raise ValueError("assessment_id must be at least 5 characters long")
        return value

    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError("user_id must not be empty")
        if len(value) > 200:
            raise ValueError("user_id must not exceed 200 characters")
        if len(value) < 5:
            raise ValueError("user_id must be at least 5 characters long")
        return value
