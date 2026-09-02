from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.features.content_management.get_all_contents.get_all_contents_handler import (
    GetAllContentsHandler,
)
from src.features.content_management.get_contents_by_topic.get_contents_by_topic_handler import (
    GetContentsByTopicHandler,
)
from src.features.content_management.get_contents_by_category.get_contents_by_category_handler import (
    GetContentsByCategoryHandler,
)
from src.features.content_management.get_contents_by_title.get_contents_by_title_handler import (
    GetContentsByTitleHandler,
)
from src.features.content_management.get_contents_by_category_topic.get_contents_by_category_topic_handler import (
    GetContentsByCategoryTopicHandler,
)
from src.features.content_management.get_learning_path_progress.get_learning_path_progress_handler import (
    GetLearningPathProgressHandler,
)
from src.features.content_management.get_recommended_content.get_recommended_content_handler import (
    GetRecommendedContentHandler,
)
from src.features.content_management.get_resource_content.get_resource_content_handler import (
    GetResourceContentHandler,
)
from src.features.content_management.get_top_best_content.get_top_best_content_handler import (
    GetTopBestContentHandler,
)
from src.features.content_management.get_top_worse_content.get_top_worse_content_handler import (
    GetTopWorseContentHandler,
)
from src.features.content_management.rate_content.rate_content_handler import (
    RateContentHandler,
)
from src.features.content_management.register_content.register_content_handler import (
    RegisterContentHandler,
)
from src.features.content_management.shared.content import ResourceContentBuilder
from src.features.content_management.shared.content_repository import (
    ResourceContentRepository,
)
from src.features.content_management.shared.learning_path_repository import (
    LearningPathRepository,
)
from src.features.content_management.update_content_path_status.update_content_path_status_handler import (
    UpdateContentPathStatusHandler,
)
from src.features.content_management.update_resource_content.update_resource_content_handler import (
    UpdateResourceContentHandler,
)
from src.features.content_management.update_resource_status.update_resource_status_handler import (
    UpdateResourceStatusHandler,
)
from itmentorsoft_persistence.mappers import (
    RateContentMapper,
    PostgresLearningPathMapper,
    ResourceContentMapper,
)
from src.infrastructure.database.postgresql.repository.postgres_learning_path_repository import (
    PostgresLearningPathRepository,
)
from src.infrastructure.database.postgresql.repository.postgres_resource_content_repository import (
    PostgresResourceContentRepository,
)
from itmentorsoft_persistence import get_db


def get_resource_content_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> PostgresResourceContentRepository:
    return PostgresResourceContentRepository(
        session_factory=session,
        mapper=ResourceContentMapper,
        rating_mapper=RateContentMapper,
    )


def get_register_content_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> RegisterContentHandler:
    return RegisterContentHandler(content_repository, ResourceContentBuilder)


def get_rate_content_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> RateContentHandler:
    return RateContentHandler(content_repository)


def get_all_contents_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> GetAllContentsHandler:
    return GetAllContentsHandler(content_repository)


def get_get_resource_content_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> GetResourceContentHandler:
    return GetResourceContentHandler(content_repository)


def get_get_contents_by_topic_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> GetContentsByTopicHandler:
    return GetContentsByTopicHandler(content_repository)


def get_get_contents_by_category_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> GetContentsByCategoryHandler:
    return GetContentsByCategoryHandler(content_repository)


def get_get_contents_by_title_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> GetContentsByTitleHandler:
    return GetContentsByTitleHandler(content_repository)


def get_get_contents_by_category_topic_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> GetContentsByCategoryTopicHandler:
    return GetContentsByCategoryTopicHandler(content_repository)


def get_update_resource_content_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> UpdateResourceContentHandler:
    return UpdateResourceContentHandler(content_repository)


def get_update_resource_status_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> UpdateResourceStatusHandler:
    return UpdateResourceStatusHandler(content_repository)


def get_learning_path_repository(
    session: Annotated[AsyncSession, Depends(get_db)],
) -> PostgresLearningPathRepository:
    return PostgresLearningPathRepository(
        session_factory=session, mapper=PostgresLearningPathMapper
    )


def get_get_recommended_content_handler(
    learning_path_repository: Annotated[
        LearningPathRepository, Depends(get_learning_path_repository)
    ],
) -> GetRecommendedContentHandler:
    return GetRecommendedContentHandler(learning_path_repository)


def get_update_content_path_status_handler(
    learning_path_repository: Annotated[
        LearningPathRepository, Depends(get_learning_path_repository)
    ],
) -> UpdateContentPathStatusHandler:
    return UpdateContentPathStatusHandler(learning_path_repository)


def get_get_learning_path_progress_handler(
    learning_path_repository: Annotated[
        LearningPathRepository, Depends(get_learning_path_repository)
    ],
) -> GetLearningPathProgressHandler:

    return GetLearningPathProgressHandler(learning_path_repository)


def get_get_top_best_content_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> GetTopBestContentHandler:
    return GetTopBestContentHandler(content_repository)


def get_get_top_worse_content_handler(
    content_repository: Annotated[
        ResourceContentRepository, Depends(get_resource_content_repository)
    ],
) -> GetTopWorseContentHandler:
    return GetTopWorseContentHandler(content_repository)
