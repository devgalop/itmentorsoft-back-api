from pydantic import BaseModel, field_validator
from src.i18n import t


class GetStudentsByCategoryRequest(BaseModel):
    category: str
    page: int
    page_size: int

    @field_validator("page")
    def validate_page(cls, value: int) -> int:
        if value < 0:
            raise ValueError(t("validation.page.non_negative"))
        return value

    @field_validator("page_size")
    def validate_page_size(cls, value: int) -> int:
        if value < 1:
            raise ValueError(t("validation.page_size.min"))
        if value > 100:
            raise ValueError(t("validation.page_size.max"))
        return value

    @field_validator("category")
    def validate_category(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.category.required"))
        if len(value) > 80:
            raise ValueError(t("validation.category.max_length_80"))
        if len(value) < 3:
            raise ValueError(t("validation.category.min_length"))
        return value
