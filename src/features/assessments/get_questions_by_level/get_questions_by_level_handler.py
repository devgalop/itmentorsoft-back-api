from src.features.assessments.get_questions_by_level.get_questions_by_level_request import (
    GetQuestionsByLevelRequest,
)
from src.features.assessments.get_questions_by_level.get_questions_by_level_response import (
    EvaluativeQuestionData,
    GetQuestionsByLevelResponse,
)
from itmentorsoft_persistence.dto import QuestionDifficulty
from itmentorsoft_persistence.repositories import (
    QuestionAssessmentRepository,
)


class GetQuestionsByLevelHandler:
    def __init__(self, question_repository: QuestionAssessmentRepository):
        self.question_repository = question_repository

    async def handle(
        self, request: GetQuestionsByLevelRequest
    ) -> GetQuestionsByLevelResponse:
        try:
            difficulty = QuestionDifficulty(request.difficulty)
            questions = await self.question_repository.get_question_by_level(difficulty)
            questions_data = [
                EvaluativeQuestionData(
                    question_id=q.question_id,
                    text_to_evaluate=q.text_to_evaluate,
                )
                for q in questions
            ]
            return GetQuestionsByLevelResponse(
                is_success=True,
                message="Questions retrieved successfully",
                questions=questions_data,
            )
        except Exception as e:
            return GetQuestionsByLevelResponse(
                is_success=False,
                message=f"An error occurred while retrieving questions: {str(e)}",
                questions=[],
            )
