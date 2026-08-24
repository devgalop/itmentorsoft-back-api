from enum import Enum
import uuid
from pydantic import BaseModel


class ContentCategory(Enum):
    """Content category

    Args:
        Enum (Enum): Enum class for content category.
    """

    NOVICE = "principiante"
    EMERGING = "básico"
    AVERAGE = "intermedio"
    PROFICIENT = "avanzado"


class TopContentOrder(Enum):
    """Top content order

    Args:
        Enum (Enum): Enum class for top content order.
    """

    DESCENDING = "desc"
    ASCENDING = "asc"


class ResourceContentResponse(BaseModel):
    """Represents a response for educational resource content

    Args:
        content_id (str): The ID of the content.
        title (str): The title of the content.
        summary (str): The summary of the content.
        url (str): The URL of the content.
        category (ContentCategory): The category of the content.
        related_topics (list[str]): The related topics of the content.
    """

    content_id: str
    title: str
    summary: str
    url: str
    category: ContentCategory
    related_topics: list[str]


class ResourceContent:
    """Represents an educational resource content"""

    def __init__(self):
        self.content_id = uuid.uuid4().hex
        self.title = ""
        self.summary = ""
        self.url = ""
        self.category = ContentCategory.NOVICE
        self.related_topics: list[str] = []

    def add_content_id(self, content_id: str):
        """Add a content ID to the content

        Args:
            content_id (str): The content ID to add.
        """
        self.content_id = content_id

    def add_title(self, title: str):
        """Add a title to the content

        Args:
            title (str): The title to add.
        """
        self.title = title

    def add_summary(self, summary: str):
        """Add a summary to the content

        Args:
            summary (str): The summary to add.
        """
        self.summary = summary

    def add_url(self, url: str):
        """Add a URL to the content

        Args:
            url (str): The URL to add.
        """
        self.url = url

    def categorize_content(self, category: ContentCategory):
        """Categorize the content

        Args:
            category (ContentCategory): The category to categorize the content.
        """
        self.category = category

    def add_related_topic(self, topic: str):
        """Add a related topic to the content

        Args:
            topic (str): The related topic to add.
        """
        self.related_topics.append(topic)


class PaginatedResourceContentResult:
    """Represents a paginated result of educational resource contents

    Args:
        items (list[ResourceContentResponse]): The list of educational resource contents for the current page.
        total (int): The total number of educational resource contents across all pages.
    """

    def __init__(self, items: list[ResourceContentResponse], total: int):
        self.items = items
        self.total = total


class ResourceContentBuilder:
    """This class provide a builder for ResourceContent class"""

    def __init__(self):
        self.content = ResourceContent()

    def set_content_id(self, content_id: str) -> "ResourceContentBuilder":
        """Set the content ID of the content

        Args:
            content_id (str): The content ID to set.
        """
        self.content.add_content_id(content_id)
        return self

    def set_title(self, title: str) -> "ResourceContentBuilder":
        """Set the title of the content

        Args:
            title (str): The title to set.
        """
        self.content.add_title(title)
        return self

    def set_summary(self, summary: str) -> "ResourceContentBuilder":
        """Set the summary of the content

        Args:
            summary (str): The summary to set.
        """
        self.content.add_summary(summary)
        return self

    def set_url(self, url: str) -> "ResourceContentBuilder":
        """Set the URL of the content

        Args:
            url (str): The URL to set.
        """
        self.content.add_url(url)
        return self

    def set_category(self, category: ContentCategory) -> "ResourceContentBuilder":
        """Set the category of the content

        Args:
            category (ContentCategory): The category to set.
        """
        self.content.categorize_content(category)
        return self

    def add_related_topics(self, topics: list[str]) -> "ResourceContentBuilder":
        """Add related topics to the content

        Args:
            topics (list[str]): The related topics to add.
        """
        for topic in topics:
            self.content.add_related_topic(topic)
        return self

    def build(self) -> ResourceContent:
        """Build the content

        Returns:
            ResourceContent: The built content.
        """
        return self.content


class ResourceContentRating:
    """Represents a rating for educational resource content

    Args:
        content_id (str): The ID of the content.
        title (str): The title of the content.
        summary (str): The summary of the content.
        rating (float): The rating of the content.
    """

    def __init__(self, content_id: str, title: str, summary: str, rating: float):
        self.content_id = content_id
        self.title = title
        self.summary = summary
        self.rating = rating
