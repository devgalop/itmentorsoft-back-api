from fastapi import APIRouter

from src.features.content_management.get_all_contents.get_all_contents_endpoint import (
    router as get_all_contents_router,
)
from src.features.content_management.get_resource_content.get_resource_content_endpoint import (
    router as get_resource_content_router,
)
from src.features.content_management.register_content.register_content_endpoint import (
    router as register_content_router,
)
from src.features.content_management.rate_content.rate_content_endpoint import (
    router as rate_content_router,
)
from src.features.content_management.get_contents_by_topic.get_contents_by_topic_endpoint import (
    router as get_contents_by_topic_router,
)
from src.features.content_management.get_contents_by_category.get_contents_by_category_endpoint import (
    router as get_contents_by_category_router,
)
from src.features.content_management.get_contents_by_title.get_contents_by_title_endpoint import (
    router as get_contents_by_title_router,
)
from src.features.content_management.get_contents_by_category_topic.get_contents_by_category_topic_endpoint import (
    router as get_contents_by_category_topic_router,
)
from src.features.content_management.update_resource_content.update_resource_content_endpoint import (
    router as update_resource_content_router,
)
from src.features.content_management.update_resource_status.update_resource_status_endpoint import (
    router as update_resource_status_router,
)
from src.features.content_management.get_recommended_content.get_recommended_content_endpoint import (
    router as get_recommended_content_router,
)
from src.features.content_management.update_content_path_status.update_content_path_status_endpoint import (
    router as update_content_path_status_router,
)
from src.features.content_management.get_learning_path_progress.get_learning_path_progress_endpoint import (
    router as get_learning_path_progress_router,
)

router = APIRouter()
router.include_router(get_all_contents_router)
router.include_router(get_resource_content_router)
router.include_router(register_content_router)
router.include_router(rate_content_router)
router.include_router(get_contents_by_topic_router)
router.include_router(get_contents_by_category_router)
router.include_router(get_contents_by_title_router)
router.include_router(get_contents_by_category_topic_router)
router.include_router(update_resource_content_router)
router.include_router(update_resource_status_router)
router.include_router(get_recommended_content_router)
router.include_router(update_content_path_status_router)
router.include_router(get_learning_path_progress_router)
