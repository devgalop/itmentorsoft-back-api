from pydantic import BaseModel, field_validator
from src.i18n import t


class GetResourceRequest(BaseModel):
    content_id: str

    @field_validator("content_id")
    def validate_content_id(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.content_id.required"))
        if len(value) > 100:
            raise ValueError(t("validation.content_id.max_length"))
        if len(value) < 10:
            raise ValueError(t("validation.content_id.min_length"))
        return value
