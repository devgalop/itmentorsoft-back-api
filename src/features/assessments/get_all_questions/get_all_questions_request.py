from pydantic import BaseModel, field_validator
from src.i18n import t


class GetAllQuestionsRequest(BaseModel):
    page: int = 0
    page_size: int = 10

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
