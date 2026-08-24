from abc import ABC, abstractmethod

from src.features.content_management.get_contents_by_category.get_contents_by_category_request import (
    GetContentsByCategoryPaginationRequest,
)
from src.features.content_management.get_contents_by_category_topic.get_contents_by_category_topic_request import (
    GetContentsByCategoryTopicPaginationRequest,
)
from src.features.content_management.get_contents_by_title.get_contents_by_title_request import (
    GetContentsByTitlePaginationRequest,
)
from src.features.content_management.get_contents_by_topic.get_contents_by_topic_request import (
    GetContentsByTopicPaginationRequest,
)
from src.features.content_management.rate_content.rate_content_request import (
    RateContent,
)
from src.features.content_management.shared.content import (
    PaginatedResourceContentResult,
    ResourceContent,
    ResourceContentRating,
    ResourceContentResponse,
)
from src.features.content_management.update_resource_content.update_resource_content_request import (
    UpdateResourceContentRequest,
)


class ResourceContentRepository(ABC):

    @abstractmethod
    async def save(self, content: ResourceContent):
        """Save educational resource content

        Args:
            content (ResourceContent): The educational resource content to be saved
        """
        pass

    @abstractmethod
    async def get_resource_content(
        self, content_id: str
    ) -> ResourceContentResponse | None:
        """Get educational resource content by content ID
        Args:
            content_id (str): The content ID of the educational resource content to be retrieved
        Returns:
            ResourceContentResponse | None: The educational resource content with the specified content ID, or None if not found
        """
        pass

    @abstractmethod
    async def get_resource_contents_by_category(
        self, request: GetContentsByCategoryPaginationRequest
    ) -> PaginatedResourceContentResult:
        """Get educational resource contents by category
        Args:
            request (GetContentsByCategoryPaginationRequest): The request containing the category and pagination information
        Returns:
            PaginatedResourceContentResult: A list of educational resource contents with the specified category
        """
        pass

    @abstractmethod
    async def get_resource_contents_by_related_topic(
        self, request: GetContentsByTopicPaginationRequest
    ) -> PaginatedResourceContentResult:
        """Get educational resource contents by related topic
        Args:
            request (GetContentsByTopicPaginationRequest): The request containing the related topic and pagination information
        Returns:
            PaginatedResourceContentResult: A list of educational resource contents with the specified related topic
        """
        pass

    @abstractmethod
    async def get_resource_contents_by_title(
        self, request: GetContentsByTitlePaginationRequest
    ) -> PaginatedResourceContentResult:
        """Get educational resource contents by title
        Args:
            request (GetContentsByTitlePaginationRequest): The request containing the title and pagination information
        Returns:
            PaginatedResourceContentResult: A list of educational resource contents with the specified title
        """
        pass

    @abstractmethod
    async def get_resource_contents_by_category_and_related_topic(
        self, request: GetContentsByCategoryTopicPaginationRequest
    ) -> PaginatedResourceContentResult:
        """Get educational resource contents by category and related topic
        Args:
            request (GetContentsByCategoryTopicPaginationRequest): The request containing the category, related topic, and pagination information
        Returns:
            PaginatedResourceContentResult: A list of educational resource contents with the specified category and related topic
        """
        pass

    @abstractmethod
    async def rate_resource_content(self, request: RateContent):
        """Rate educational resource content
        Args:
            request (RateContent): The request containing the content ID, user ID, rating, and optional comment for rating the educational resource content
        """
        pass

    @abstractmethod
    async def get_all_resource_contents(
        self, page: int, page_size: int
    ) -> PaginatedResourceContentResult:
        """Get all educational resource contents with pagination
        Args:
            page (int): The zero-based page index.
            page_size (int): The number of items per page.
        Returns:
            PaginatedResourceContentResult: The paginated result containing the items for the requested page and the total count of all records.
        """
        pass

    @abstractmethod
    async def update_resource_content(
        self, content_id: str, request: UpdateResourceContentRequest
    ):
        """Update educational resource content
        Args:
            content_id (str): The content ID of the educational resource content to be updated
            request (UpdateResourceContentRequest): The request containing the updated information for the educational resource content
        """
        pass

    @abstractmethod
    async def update_resource_status(self, content_id: str, new_status: bool) -> bool:
        """Update the status of an educational resource content
        Args:
            content_id (str): The content ID of the educational resource content to be updated
            new_status (bool): The new status to be set for the educational resource content
        Returns:
            bool: True if the update was successful, False otherwise
        """
        pass

    @abstractmethod
    async def get_top_content(
        self, topic: str, limit: int, order: str = "desc"
    ) -> list[ResourceContentRating]:
        """Get the top educational resource contents based on rating for a specific topic
        Args:
            topic (str): The topic to filter the educational resource contents
            limit (int): The maximum number of top educational resource contents to retrieve
            order (str): The order of the ratings, either "desc" for descending or "asc" for ascending
        Returns:
            list[ResourceContentRating]: A list of the top educational resource contents based on rating for the specified topic
        """
        pass
