from src.i18n import t
from src.features.assessments.get_question_categories.get_question_categories_request import (
    GetQuestionCategoriesRequest,
)
from src.features.assessments.get_question_categories.get_question_categories_response import (
    GetQuestionCategoriesResponse,
)
from itmentorsoft_persistence.repositories import QuestionRepository


class GetQuestionCategoriesHandler:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    async def handle(
        self, request: GetQuestionCategoriesRequest
    ) -> GetQuestionCategoriesResponse:
        categories = await self.question_repository.get_question_categories(
            request.version
        )
        if not categories:
            return GetQuestionCategoriesResponse(
                is_success=False,
                message=t("question.categories.retrieval_failed"),
                categories=[],
            )
        return GetQuestionCategoriesResponse(
            is_success=True,
            message=t("question.categories.retrieved"),
            categories=categories,
        )
