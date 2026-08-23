from pydantic import BaseModel, field_validator


class GetLearningPathProgressRequest(BaseModel):
    path_id: str

    @field_validator("path_id")
    def validate_path_id(cls, value: str) -> str:
        if not value:
            raise ValueError("path_id is required.")
        if len(value) < 5:
            raise ValueError("path_id must be at least 5 characters long.")
        if len(value) > 100:
            raise ValueError("path_id must not exceed 100 characters.")
        return value
