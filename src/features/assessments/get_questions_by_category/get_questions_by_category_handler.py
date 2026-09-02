from src.features.assessments.get_questions_by_category.get_questions_by_category_request import (
    GetQuestionsByCategoryRequest,
)
from src.features.assessments.get_questions_by_category.get_questions_by_category_response import (
    GetQuestionsByCategoryResponse,
    QuestionByCategoryData,
)
from itmentorsoft_persistence.repositories import (
    QuestionAssessmentRepository,
)


class GetQuestionsByCategoryHandler:
    def __init__(self, question_repository: QuestionAssessmentRepository):
        self.question_repository = question_repository

    async def handle(
        self, request: GetQuestionsByCategoryRequest
    ) -> GetQuestionsByCategoryResponse:
        try:
            questions = await self.question_repository.get_questions_by_category(
                request.category
            )
            questions_data = [
                QuestionByCategoryData(
                    question_id=q.question_id,
                    text_to_evaluate=q.text_to_evaluate,
                )
                for q in questions
            ]
            return GetQuestionsByCategoryResponse(
                is_success=True,
                message="Questions retrieved successfully",
                questions=questions_data,
            )
        except Exception as e:
            return GetQuestionsByCategoryResponse(
                is_success=False,
                message=f"An error occurred while retrieving questions: {str(e)}",
                questions=[],
            )
