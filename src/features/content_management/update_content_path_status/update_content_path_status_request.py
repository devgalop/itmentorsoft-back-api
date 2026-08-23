from pydantic import BaseModel, field_validator


class UpdateContentPathStatusRequest(BaseModel):
    path_id: str
    content_id: str
    status: bool

    @field_validator("path_id")
    def validate_path_id(cls, value: str) -> str:
        if not value:
            raise ValueError("path_id must not be empty")
        if len(value) < 5:
            raise ValueError("path_id must be at least 5 characters long")
        if len(value) > 100:
            raise ValueError("path_id must not exceed 100 characters")
        return value

    @field_validator("content_id")
    def validate_content_id(cls, value: str) -> str:
        if not value:
            raise ValueError("content_id must not be empty")
        if len(value) < 5:
            raise ValueError("content_id must be at least 5 characters long")
        if len(value) > 100:
            raise ValueError("content_id must not exceed 100 characters")
        return value

    @field_validator("status")
    def validate_status(cls, value: bool) -> bool:
        if not isinstance(value, bool):
            raise ValueError("status must be a boolean value")
        return value
