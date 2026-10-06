from pydantic import BaseModel

from src.features.content_management.shared.learning_path_manager_service import (
    TopicPathAssociation,
)


class GenerateLearningPathResponse(BaseModel):
    is_success: bool
    message: str
    learning_path: list[TopicPathAssociation] | None = None
