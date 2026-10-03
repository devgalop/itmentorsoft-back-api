from pydantic import BaseModel, field_validator
from src.i18n import t


class GetContentsByTitleRequest(BaseModel):
    title: str

    @field_validator("title")
    def validate_title(cls, value: str) -> str:
        if not value.strip():
            raise ValueError(t("validation.title.required"))
        if len(value) > 100:
            raise ValueError(t("validation.title.max_length_100"))
        if len(value) < 3:
            raise ValueError(t("validation.title.min_length_3"))
        return value.strip()


class GetContentsByTitlePaginationRequest(GetContentsByTitleRequest):
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
