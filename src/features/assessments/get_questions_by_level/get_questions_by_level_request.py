from pydantic import BaseModel, field_validator

from itmentorsoft_persistence.dto import QuestionDifficulty


class GetQuestionsByLevelRequest(BaseModel):
    difficulty: str

    @field_validator("difficulty")
    def validate_difficulty(cls, value: str) -> str:
        if not value:
            raise ValueError("Difficulty cannot be empty")
        valid_values = [d.value for d in QuestionDifficulty]
        if value not in valid_values:
            raise ValueError(
                f"Invalid difficulty. Must be one of: {', '.join(valid_values)}"
            )
        return value
