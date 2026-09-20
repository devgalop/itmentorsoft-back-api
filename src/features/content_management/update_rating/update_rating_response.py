from pydantic import BaseModel


class UpdateRatingResponse(BaseModel):
    is_success: bool
    message: str
