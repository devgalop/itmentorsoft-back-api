from pydantic import BaseModel, field_validator
from src.i18n import t


class QuestionRubric(BaseModel):
    score: int
    criteria: str

    @field_validator("score")
    def validate_score(cls, value: int) -> int:
        if value < 0 or value > 3:
            raise ValueError(t("validation.score.range"))
        return value

    @field_validator("criteria")
    def validate_criteria(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.criteria.required"))
        if len(value) > 300:
            raise ValueError(t("validation.criteria.max_length"))
        if len(value) < 10:
            raise ValueError(t("validation.criteria.min_length"))
        return value


class RegisterQuestionRequest(BaseModel):
    text: str
    concept: str
    definition: str
    simple_explanation: str
    correct_sample: str
    wrong_sample: str
    common_misconception: list[str]
    rubric: list[QuestionRubric]
    semantic_keywords: list[str]
    difficulty: str
    topic: str
    version: int = 1
    previous_version_id: str | None = None
    root_version_id: str | None = None

    @field_validator("text")
    def validate_text(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.text.required"))
        if len(value) > 500:
            raise ValueError(t("validation.text.max_length"))
        if len(value) < 20:
            raise ValueError(t("validation.text.min_length"))
        return value

    @field_validator("concept")
    def validate_concept(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.concept.required"))
        if len(value) > 150:
            raise ValueError(t("validation.concept.max_length"))
        if len(value) < 10:
            raise ValueError(t("validation.concept.min_length"))
        return value

    @field_validator("definition")
    def validate_definition(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.definition.required"))
        if len(value) > 500:
            raise ValueError(t("validation.definition.max_length"))
        if len(value) < 20:
            raise ValueError(t("validation.definition.min_length"))
        return value

    @field_validator("simple_explanation")
    def validate_simple_explanation(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.simple_explanation.required"))
        if len(value) > 300:
            raise ValueError(t("validation.simple_explanation.max_length"))
        if len(value) < 20:
            raise ValueError(t("validation.simple_explanation.min_length"))
        return value

    @field_validator("correct_sample")
    def validate_correct_sample(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.correct_sample.required"))
        if len(value) > 300:
            raise ValueError(t("validation.correct_sample.max_length"))
        if len(value) < 20:
            raise ValueError(t("validation.correct_sample.min_length"))
        return value

    @field_validator("wrong_sample")
    def validate_wrong_sample(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.wrong_sample.required"))
        if len(value) > 300:
            raise ValueError(t("validation.wrong_sample.max_length"))
        if len(value) < 20:
            raise ValueError(t("validation.wrong_sample.min_length"))
        return value

    @field_validator("common_misconception")
    def validate_common_misconception(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError(t("validation.common_misconception.required"))
        if len(value) < 2:
            raise ValueError(t("validation.common_misconception.min_items"))
        for item in value:
            if len(item) > 300:
                raise ValueError(t("validation.common_misconception.item_max_length"))
            if len(item) < 20:
                raise ValueError(t("validation.common_misconception.item_min_length"))
        return value

    @field_validator("semantic_keywords")
    def validate_semantic_keywords(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError(t("validation.semantic_keywords.required"))
        if len(value) < 1:
            raise ValueError(t("validation.semantic_keywords.min_items"))
        for item in value:
            if len(item) > 100:
                raise ValueError(t("validation.semantic_keywords.item_max_length"))
            if len(item) < 2:
                raise ValueError(t("validation.semantic_keywords.item_min_length"))
        return value

    @field_validator("difficulty")
    def validate_difficulty(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.difficulty.required"))
        if len(value) > 30:
            raise ValueError(t("validation.difficulty.max_length"))
        if len(value) < 4:
            raise ValueError(t("validation.difficulty.min_length"))
        return value

    @field_validator("topic")
    def validate_topic(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.topic.required"))
        if len(value) > 100:
            raise ValueError(t("validation.topic.max_length"))
        if len(value) < 2:
            raise ValueError(t("validation.topic.min_length"))
        return value

    @field_validator("previous_version_id")
    def validate_previous_version_id(cls, value: str | None) -> str | None:
        if value is not None and len(value) > 100:
            raise ValueError(t("validation.previous_version_id.max_length"))
        return value

    @field_validator("root_version_id")
    def validate_root_version_id(cls, value: str | None) -> str | None:
        if value is not None and len(value) > 100:
            raise ValueError(t("validation.root_version_id.max_length"))
        return value
