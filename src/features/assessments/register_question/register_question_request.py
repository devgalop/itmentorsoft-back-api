from pydantic import BaseModel, field_validator


class QuestionRubric(BaseModel):
    score: int
    criteria: str

    @field_validator("score")
    def validate_score(cls, value: int) -> int:
        if value < 0 or value > 3:
            raise ValueError("Score must be between 0 and 3")
        return value

    @field_validator("criteria")
    def validate_criteria(cls, value: str) -> str:
        if not value:
            raise ValueError("Criteria cannot be empty")
        if len(value) > 300:
            raise ValueError("Criteria cannot be longer than 300 characters")
        if len(value) < 10:
            raise ValueError("Criteria must be at least 10 characters long")
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

    @field_validator("text")
    def validate_text(cls, value: str) -> str:
        if not value:
            raise ValueError("Text cannot be empty")
        if len(value) > 500:
            raise ValueError("Text cannot be longer than 500 characters")
        if len(value) < 20:
            raise ValueError("Text must be at least 20 characters long")
        return value

    @field_validator("concept")
    def validate_concept(cls, value: str) -> str:
        if not value:
            raise ValueError("Concept cannot be empty")
        if len(value) > 150:
            raise ValueError("Concept cannot be longer than 150 characters")
        if len(value) < 10:
            raise ValueError("Concept must be at least 10 characters long")
        return value

    @field_validator("definition")
    def validate_definition(cls, value: str) -> str:
        if not value:
            raise ValueError("Definition cannot be empty")
        if len(value) > 500:
            raise ValueError("Definition cannot be longer than 500 characters")
        if len(value) < 20:
            raise ValueError("Definition must be at least 20 characters long")
        return value

    @field_validator("simple_explanation")
    def validate_simple_explanation(cls, value: str) -> str:
        if not value:
            raise ValueError("Simple explanation cannot be empty")
        if len(value) > 300:
            raise ValueError("Simple explanation cannot be longer than 300 characters")
        if len(value) < 20:
            raise ValueError("Simple explanation must be at least 20 characters long")
        return value

    @field_validator("correct_sample")
    def validate_correct_sample(cls, value: str) -> str:
        if not value:
            raise ValueError("Correct sample cannot be empty")
        if len(value) > 300:
            raise ValueError("Correct sample cannot be longer than 300 characters")
        if len(value) < 20:
            raise ValueError("Correct sample must be at least 20 characters long")
        return value

    @field_validator("wrong_sample")
    def validate_wrong_sample(cls, value: str) -> str:
        if not value:
            raise ValueError("Wrong sample cannot be empty")
        if len(value) > 300:
            raise ValueError("Wrong sample cannot be longer than 300 characters")
        if len(value) < 20:
            raise ValueError("Wrong sample must be at least 20 characters long")
        return value

    @field_validator("common_misconception")
    def validate_common_misconception(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("Common misconception cannot be empty")
        if len(value) < 2:
            raise ValueError("Common misconception must have at least 2 items")
        for item in value:
            if len(item) > 300:
                raise ValueError(
                    "Each common misconception cannot be longer than 300 characters"
                )
            if len(item) < 20:
                raise ValueError(
                    "Each common misconception must be at least 20 characters long"
                )
        return value

    @field_validator("semantic_keywords")
    def validate_semantic_keywords(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("Semantic keywords cannot be empty")
        if len(value) < 1:
            raise ValueError("Semantic keywords must have at least 1 item")
        for item in value:
            if len(item) > 100:
                raise ValueError(
                    "Each semantic keyword cannot be longer than 100 characters"
                )
            if len(item) < 2:
                raise ValueError(
                    "Each semantic keyword must be at least 2 characters long"
                )
        return value

    @field_validator("difficulty")
    def validate_difficulty(cls, value: str) -> str:
        if not value:
            raise ValueError("Difficulty cannot be empty")
        if len(value) > 30:
            raise ValueError("Difficulty cannot be longer than 30 characters")
        if len(value) < 4:
            raise ValueError("Difficulty must be at least 4 characters long")
        return value

    @field_validator("topic")
    def validate_topic(cls, value: str) -> str:
        if not value:
            raise ValueError("Topic cannot be empty")
        if len(value) > 100:
            raise ValueError("Topic cannot be longer than 100 characters")
        if len(value) < 2:
            raise ValueError("Topic must be at least 2 characters long")
        return value
