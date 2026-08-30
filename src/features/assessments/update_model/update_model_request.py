from pydantic import BaseModel, field_validator


class UpdateModelRequest(BaseModel):
    process: str
    model_id: str

    @field_validator("process")
    def validate_process(cls, value: str) -> str:
        if not value:
            raise ValueError("Process cannot be empty")
        if len(value) < 3:
            raise ValueError("Process must be at least 3 characters long")
        if len(value) > 50:
            raise ValueError("Process cannot exceed 50 characters")
        return value

    @field_validator("model_id")
    def validate_model_id(cls, value: str) -> str:
        if not value:
            raise ValueError("Model ID cannot be empty")
        if len(value) < 5:
            raise ValueError("Model ID must be at least 5 characters long")
        if len(value) > 20:
            raise ValueError("Model ID cannot exceed 20 characters")
        return value
