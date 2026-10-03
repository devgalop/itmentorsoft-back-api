from pydantic import BaseModel, field_validator
from src.i18n import t


class GetContentsByCategoryTopicRequest(BaseModel):
    category: str
    topic: str

    @field_validator("category")
    def validate_category(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(t("validation.category.required"))
        if len(value) > 100:
            raise ValueError(t("validation.category.max_length_100"))
        if len(value) < 3:
            raise ValueError(t("validation.category.min_length"))
        return value.strip()

    @field_validator("topic")
    def validate_topic(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(t("validation.topic.required"))
        if len(value) > 100:
            raise ValueError(t("validation.topic.max_length"))
        if len(value) < 3:
            raise ValueError(t("validation.topic.min_length"))
        return value.strip()


class GetContentsByCategoryTopicPaginationRequest(GetContentsByCategoryTopicRequest):
    page: int = 0
    page_size: int = 10

    @field_validator("page")
    def validate_page(cls, value: int) -> int:
        if value < 0:
            raise ValueError(t("validation.page.non_negative"))
        return value

    @field_validator("page_size")
    def validate_page_size(cls, value: int) -> int:
        if value < 1 or value > 100:
            raise ValueError(t("validation.page_size.range"))
        return value
