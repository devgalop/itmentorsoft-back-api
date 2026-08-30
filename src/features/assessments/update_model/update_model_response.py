from pydantic import BaseModel


class UpdateModelResponse(BaseModel):
    is_success: bool
    message: str
