from pydantic import BaseModel, field_validator
from src.i18n import t


class GetUsersByRoleRequest(BaseModel):
    role: str

    @field_validator("role")
    def validate_role(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.role.required"))
        if len(value) < 3:
            raise ValueError(t("validation.role.min_length"))
        if len(value) > 20:
            raise ValueError(t("validation.role.max_length"))
        return value
