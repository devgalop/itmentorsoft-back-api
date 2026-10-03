from pydantic import BaseModel, field_validator
from src.i18n import t


class GetCategorySummaryRequest(BaseModel):
    category: str

    @field_validator("category")
    def validate_category(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.category.required"))
        if len(value) > 80:
            raise ValueError(t("validation.category.max_length_80"))
        if len(value) < 3:
            raise ValueError(t("validation.category.min_length"))
        return value.strip()
