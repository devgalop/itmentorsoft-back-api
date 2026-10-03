from src.i18n import t
from src.features.assessments.get_questions_topics.get_questions_topics_response import (
    GetQuestionsTopicsResponse,
)
from itmentorsoft_persistence.repositories import QuestionRepository


class GetQuestionsTopicsHandler:
    def __init__(self, questions_repository: QuestionRepository):
        self.questions_repository = questions_repository

    async def handle(self) -> GetQuestionsTopicsResponse:
        topics = await self.questions_repository.get_questions_topics()
        if not topics:
            return GetQuestionsTopicsResponse(
                is_success=False,
                message=t("question.topic.none_found"),
                topics=[],
            )

        return GetQuestionsTopicsResponse(
            is_success=True,
            message=t("question.topic.published.retrieved"),
            topics=topics,
        )
