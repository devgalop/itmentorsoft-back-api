from pydantic import BaseModel


class UserByRole(BaseModel):
    user_id: str
    role: str


class GetUsersByRoleResponse(BaseModel):
    is_success: bool
    message: str
    total_users: int
    users: list[UserByRole]
