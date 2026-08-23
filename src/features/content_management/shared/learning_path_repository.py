from abc import ABC, abstractmethod

from src.features.content_management.shared.learning_path import (
    LearningPath,
    LearningPathResponse,
)


class LearningPathRepository(ABC):

    @abstractmethod
    async def get_learning_path(self, user_id: str) -> LearningPathResponse:
        """Get a learning path for a user

        Args:
            user_id (str): The ID of the user whose learning path is to be retrieved

        Returns:
            LearningPathResponse: The learning path for the user, or None if not found
        """
        pass

    @abstractmethod
    async def save_learning_path(self, learning_path: LearningPath):
        """Save a learning path for a user

        Args:
            learning_path (LearningPath): The learning path to be saved

        Returns:
            None
        """
        pass
