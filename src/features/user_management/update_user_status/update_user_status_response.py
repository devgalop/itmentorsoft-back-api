from pydantic import BaseModel


class UpdateUserStatusResponse(BaseModel):
    is_success: bool
    message: str
