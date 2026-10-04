from src.i18n import t
from itmentorsoft_persistence import QuestionRepository

from src.features.assessments.get_all_questions_by_versions.get_all_questions_by_versions_request import (
    GetAllQuestionsByVersionsRequest,
)
from src.features.assessments.get_all_questions_by_versions.get_all_questions_by_versions_response import (
    GetAllQuestionsByVersionsResponse,
)


class GetAllQuestionsByVersionsHandler:
    def __init__(self, question_repository: QuestionRepository):
        self._question_repository = question_repository

    async def handle(
        self, request: GetAllQuestionsByVersionsRequest
    ) -> GetAllQuestionsByVersionsResponse:
        result = await self._question_repository.get_latest_versions_all_questions(
            page=request.page, page_size=request.page_size
        )
        if not result or not result.items:
            return GetAllQuestionsByVersionsResponse(
                is_success=False,
                message=t("question.list.none_found"),
                questions=[],
                total=0,
            )

        return GetAllQuestionsByVersionsResponse(
            is_success=True,
            message=t("question.list.retrieved"),
            questions=result.items,
            total=result.total,
        )
