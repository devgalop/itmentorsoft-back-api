from pydantic import BaseModel


class GetLearningPathProgressResponse(BaseModel):
    is_success: bool
    message: str
    path_progress: float
