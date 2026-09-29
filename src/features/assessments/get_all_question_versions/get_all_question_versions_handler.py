from itmentorsoft_persistence import QuestionRepository

from src.features.assessments.get_all_question_versions.get_all_question_versions_request import (
    GetAllQuestionVersionsRequest,
)
from src.features.assessments.get_all_question_versions.get_all_question_versions_response import (
    GetAllQuestionVersionsResponse,
)


class GetAllQuestionVersionsHandler:
    def __init__(self, questions_repository: QuestionRepository):
        self.questions_repository = questions_repository

    async def handle(
        self, request: GetAllQuestionVersionsRequest
    ) -> GetAllQuestionVersionsResponse:
        question_versions = (
            await self.questions_repository.get_all_versions_by_question(
                request.question_id
            )
        )
        if not question_versions:
            return GetAllQuestionVersionsResponse(
                is_success=False,
                message="No question versions found.",
                questions=[],
                total=0,
            )

        return GetAllQuestionVersionsResponse(
            is_success=True,
            message="Successfully retrieved all question versions.",
            questions=question_versions,
            total=len(question_versions),
        )
