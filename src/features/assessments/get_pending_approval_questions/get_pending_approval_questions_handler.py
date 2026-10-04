from src.i18n import t
from src.features.assessments.get_pending_approval_questions.get_pending_approval_questions_request import (
    GetPendingApprovalQuestionsRequest,
)
from src.features.assessments.get_pending_approval_questions.get_pending_approval_questions_response import (
    GetPendingApprovalQuestionsResponse,
)
from itmentorsoft_persistence.repositories import QuestionRepository


class GetPendingApprovalQuestionsHandler:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    async def handle(
        self, request: GetPendingApprovalQuestionsRequest
    ) -> GetPendingApprovalQuestionsResponse:
        try:
            pending_questions = (
                await self.question_repository.get_questions_pending_review(
                    request.page, request.page_size
                )
            )
            if not pending_questions:
                return GetPendingApprovalQuestionsResponse(
                    is_success=False,
                    message=t("question.pending_approval.retrieval_failed"),
                    questions=[],
                    total=0,
                )
            if pending_questions.total == 0:
                return GetPendingApprovalQuestionsResponse(
                    is_success=True,
                    message=t("question.pending_approval.none_found"),
                    questions=[],
                    total=0,
                )
            return GetPendingApprovalQuestionsResponse(
                is_success=True,
                message=t("question.pending_approval.retrieved"),
                questions=pending_questions.items,
                total=pending_questions.total,
            )
        except Exception as e:
            return GetPendingApprovalQuestionsResponse(
                is_success=False,
                message=t("question.pending_approval.invalid_request", error=str(e)),
                questions=[],
                total=0,
            )
