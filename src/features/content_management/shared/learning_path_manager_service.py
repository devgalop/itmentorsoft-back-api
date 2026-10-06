from pydantic import BaseModel
from src.i18n.messages import t
from itmentorsoft_persistence import LearningPathRepository, UserRepository


class ContentByTopic(BaseModel):
    content_id: str
    title: str
    description: str
    rating: float


class TopicSummary(BaseModel):
    topic_path_id: str
    topic: str
    contents: list[ContentByTopic]
    progress: float = 0.0


class TopicPathAssociation(BaseModel):
    topic_path_id: str
    topic: str


class LearningPathCreatedResponse(BaseModel):
    is_success: bool
    message: str
    topic_paths: list[TopicPathAssociation]


class LearningPathResponse(BaseModel):
    is_success: bool
    message: str
    learning_path: TopicSummary | None


class LearningPathManagerService:

    def __init__(
        self,
        user_repository: UserRepository,
        learning_path_repository: LearningPathRepository,
    ):
        self.user_repository = user_repository
        self.learning_path_repository = learning_path_repository

    async def create_learning_path(self, user_id: str) -> LearningPathCreatedResponse:
        """
        Create a new learning path for the specified user.

        Args:
            user_id (str): User identifier

        Returns:
            LearningPathCreatedResponse: Response containing the status, message, and the created learning path topic paths if successful.
        """
        user_found = await self.user_repository.get_user_by_id(user_id)
        if not user_found:
            return LearningPathCreatedResponse(
                is_success=False, message=t("student.not_found"), topic_paths=[]
            )

        learning_path_exists = (
            await self.learning_path_repository.is_learning_path_created(user_id)
        )
        if learning_path_exists:
            return LearningPathCreatedResponse(
                is_success=False, message=t("learning_path.exists"), topic_paths=[]
            )

        learning_path_created = await self.learning_path_repository.get_learning_path(
            user_id
        )

        if not learning_path_created:
            return LearningPathCreatedResponse(
                is_success=False, message=t("learning_path.failed"), topic_paths=[]
            )

        for path in learning_path_created.recommendation:
            await self.learning_path_repository.save_learning_path(path)

        return LearningPathCreatedResponse(
            is_success=True,
            message=t("learning_path.created"),
            topic_paths=[
                TopicPathAssociation(topic_path_id=topic.path_id, topic=topic.topic)
                for topic in learning_path_created.recommendation
            ],
        )

    async def check_path_association(self, user_id: str, path_id: str) -> bool:
        """
        Check if a learning path is associated with the specified user.

        Args:
            user_id (str): User identifier
            path_id (str): Learning path identifier

        Returns:
            bool: True if the learning path is associated with the user, False otherwise.
        """
        return await self.learning_path_repository.is_path_associated_with_user(
            path_id, user_id
        )

    async def get_learning_path(self, path_id: str) -> LearningPathResponse:
        learning_path_created = (
            await self.learning_path_repository.get_learning_path_by_id(path_id)
        )

        if not learning_path_created:
            return LearningPathResponse(
                is_success=False,
                message=t("learning_path.not_found"),
                learning_path=None,
            )

        learning_path = TopicSummary(
            topic_path_id=learning_path_created.path_id,
            topic=learning_path_created.topic,
            contents=[
                ContentByTopic(
                    content_id=content.content_id,
                    title=content.title,
                    description=content.description,
                    rating=content.rating,
                )
                for content in learning_path_created.contents
            ],
            progress=learning_path_created.progress,
        )
        return LearningPathResponse(
            is_success=True,
            message=t("learning_path.retrieved"),
            learning_path=learning_path,
        )
