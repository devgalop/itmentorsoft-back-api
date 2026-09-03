import uuid

from src.features.assessments.save_review_question.save_review_question_request import (
    SaveReviewQuestionRequest,
)
from src.features.assessments.save_review_question.save_review_question_response import (
    SaveReviewQuestionResponse,
)
from itmentorsoft_persistence.dto import QuestionReview
from itmentorsoft_persistence.repositories import QuestionRepository, UserRepository


class ReviewQuestionService:
    def __init__(
        self, user_repository: UserRepository, question_repository: QuestionRepository
    ):
        self.user_repository = user_repository
        self.question_repository = question_repository

    async def review_question(
        self, request: SaveReviewQuestionRequest
    ) -> SaveReviewQuestionResponse:
        user = await self.user_repository.get_user_by_id(request.reviewer_id)
        if not user:
            return SaveReviewQuestionResponse(
                is_success=False,
                message=f"Reviewer with ID {request.reviewer_id} does not exist.",
            )

        question = await self.question_repository.get_question(request.question_id)
        if not question:
            return SaveReviewQuestionResponse(
                is_success=False,
                message=f"Question with ID {request.question_id} does not exist.",
            )

        await self.question_repository.save_review(
            review=QuestionReview(
                review_id=uuid.uuid4().hex,
                question_id=request.question_id,
                reviewer_id=request.reviewer_id,
                review_comments=request.review_comments,
            )
        )

        await self.question_repository.update_status(
            question_id=request.question_id, status=request.status
        )

        return SaveReviewQuestionResponse(
            is_success=True, message="Review comments saved successfully."
        )
