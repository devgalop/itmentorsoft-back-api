from pydantic import BaseModel, field_validator
from src.i18n import t


class SaveReviewQuestionRequest(BaseModel):
    question_id: str
    reviewer_id: str
    review_comments: str
    status: str

    @field_validator("question_id")
    def validate_question_id(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.question_id.required"))
        if len(value) < 5:
            raise ValueError(t("validation.question_id.min_length"))
        if len(value) > 100:
            raise ValueError(t("validation.question_id.max_length"))
        return value

    @field_validator("reviewer_id")
    def validate_reviewer_id(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.reviewer_id.required"))
        if len(value) < 5:
            raise ValueError(t("validation.reviewer_id.min_length"))
        if len(value) > 100:
            raise ValueError(t("validation.reviewer_id.max_length"))
        return value

    @field_validator("review_comments")
    def validate_review_comments(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.review_comments.required"))
        if len(value) < 10:
            raise ValueError(t("validation.review_comments.min_length"))
        if len(value) > 1000:
            raise ValueError(t("validation.review_comments.max_length"))
        return value

    @field_validator("status")
    def validate_status(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.status.required"))
        return value
