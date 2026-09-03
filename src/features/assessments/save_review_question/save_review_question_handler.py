from src.features.assessments.save_review_question.save_review_question_request import (
    SaveReviewQuestionRequest,
)
from src.features.assessments.save_review_question.save_review_question_response import (
    SaveReviewQuestionResponse,
)
from itmentorsoft_persistence.dto import QuestionStatus
from src.features.assessments.shared.review_question_service import (
    ReviewQuestionService,
)


class SaveReviewQuestionHandler:
    def __init__(self, review_service: ReviewQuestionService):
        self.review_service = review_service

    async def handle(
        self, request: SaveReviewQuestionRequest
    ) -> SaveReviewQuestionResponse:
        valid_statuses = [status.value for status in QuestionStatus]
        if request.status not in valid_statuses:
            return SaveReviewQuestionResponse(
                is_success=False,
                message=f"Invalid status '{request.status}'. Valid statuses are: {', '.join(valid_statuses)}",
            )
        return await self.review_service.review_question(request)
