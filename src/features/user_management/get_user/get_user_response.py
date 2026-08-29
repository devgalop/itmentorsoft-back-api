from pydantic import BaseModel


class UserResponse(BaseModel):
    user_id: str
    username: str
    email: str
    name: str
    role: str


class GetUserResponse(BaseModel):
    is_success: bool
    message: str
    user: UserResponse | None = None
