from pydantic import BaseModel, field_validator


class GetUsersByRoleRequest(BaseModel):
    role: str

    @field_validator("role")
    def validate_role(cls, value: str) -> str:
        if not value:
            raise ValueError("Role must not be empty")
        if len(value) < 3:
            raise ValueError("Role must be at least 3 characters long")
        if len(value) > 20:
            raise ValueError("Role must be no more than 20 characters long")
        return value
