from pydantic import BaseModel, field_validator
from src.i18n import t


class AssignRoleToUserCommand:
    def __init__(self, user_id: str, role_id: str):
        self.user_id = user_id
        self.role_id = role_id


class AssignRoleRequest(BaseModel):
    user_id: str
    role: str

    @field_validator("user_id")
    def validate_user_id(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.user_id.required"))
        if len(value) < 3:
            raise ValueError("User ID must be at least 3 characters long")
        if len(value) > 100:
            raise ValueError(t("validation.user_id.max_length"))
        return value

    @field_validator("role")
    def validate_role(cls, value: str) -> str:
        if not value:
            raise ValueError(t("validation.role.required"))
        if len(value) < 3:
            raise ValueError(t("validation.role.min_length"))
        if len(value) > 50:
            raise ValueError("Role must be no more than 50 characters long")
        return value
