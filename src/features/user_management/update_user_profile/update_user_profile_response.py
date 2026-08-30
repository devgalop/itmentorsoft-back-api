from pydantic import BaseModel


class UpdateUserProfileResponse(BaseModel):
    is_success: bool
    message: str
