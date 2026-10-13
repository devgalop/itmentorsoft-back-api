from pydantic import BaseModel

from src.features.content_management.shared.learning_path_manager_service import (
    TopicSummary,
)


class GetCompleteLearningPathResponse(BaseModel):
    is_success: bool
    message: str
    learning_path: list[TopicSummary] | None
