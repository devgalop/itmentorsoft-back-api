from abc import ABC, abstractmethod

from src.features.content_management.shared.learning_path import (
    LearningPath,
    LearningPathProgressResponse,
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

    @abstractmethod
    async def update_status_content_path(
        self, path_id: str, content_id: str, status: bool
    ) -> LearningPathProgressResponse:
        """Update the status of a content path for a user

        Args:
            path_id (str): The ID of the learning path
            content_id (str): The ID of the content whose status is to be updated
            status (bool): The new status of the content
        Returns:
            LearningPathProgressResponse: The updated progress of the learning path for the user
        """
        pass

    @abstractmethod
    async def get_learning_path_progress(
        self, path_id: str
    ) -> LearningPathProgressResponse:
        """Get the progress of a learning path for a user

        Args:
            path_id (str): The ID of the learning path whose progress is to be retrieved
        Returns:
            LearningPathProgressResponse: The progress of the learning path for the user, or None if not found
        """
        pass
