from pydantic import BaseModel, field_validator
from src.i18n import t


class UpdateResourceContentRequest(BaseModel):
    title: str
    description: str
    url: str
    category: str
    related_topic: list[str]

    @field_validator("title")
    def validate_title(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.title.required"))
        if len(value) < 5:
            raise ValueError(t("validation.title.min_length_5"))
        if len(value) > 150:
            raise ValueError(t("validation.title.max_length_150"))
        return value

    @field_validator("description")
    def validate_description(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.description.required"))
        if len(value) < 10:
            raise ValueError(t("validation.description.min_length"))
        if len(value) > 300:
            raise ValueError(t("validation.description.max_length"))
        return value

    @field_validator("url")
    def validate_url(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.url.required"))
        if not value.startswith("https://"):
            raise ValueError(t("validation.url.format"))
        return value
