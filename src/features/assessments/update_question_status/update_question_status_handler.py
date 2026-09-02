from itmentorsoft_persistence.repositories import QuestionRepository
from src.features.assessments.update_question_status.update_question_status_request import (
    UpdateQuestionStatusRequest,
)
from src.features.assessments.update_question_status.update_question_status_response import (
    UpdateQuestionStatusResponse,
)


class UpdateQuestionStatusHandler:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    async def handle(
        self, request: UpdateQuestionStatusRequest
    ) -> UpdateQuestionStatusResponse:
        result = await self.question_repository.update_question_status(
            request.question_id, request.status
        )
        if not result:
            return UpdateQuestionStatusResponse(
                is_success=False,
                message=f"Question with ID {request.question_id} not found",
                question_id="",
                new_status=False,
            )
        return UpdateQuestionStatusResponse(
            is_success=result,
            message="Question status updated successfully",
            question_id=request.question_id,
            new_status=request.status,
        )
