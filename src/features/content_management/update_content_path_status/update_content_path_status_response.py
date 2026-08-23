from pydantic import BaseModel


class UpdateContentPathStatusResponse(BaseModel):
    is_success: bool
    message: str
    path_progress: float
