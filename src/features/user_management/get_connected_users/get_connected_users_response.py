from pydantic import BaseModel


class GetConnectedUsersResponse(BaseModel):
    is_success: bool
    message: str
    total_users: int
