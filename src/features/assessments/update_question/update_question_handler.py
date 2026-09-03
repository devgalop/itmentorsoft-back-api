from itmentorsoft_persistence.dto import QuestionRubricScore
from itmentorsoft_persistence.repositories import QuestionRepository
from src.features.assessments.update_question.update_question_request import (
    UpdateQuestionRequest,
)
from src.features.assessments.update_question.update_question_response import (
    UpdateQuestionResponse,
)


class UpdateQuestionHandler:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    async def handle(
        self, question_id: str, request: UpdateQuestionRequest
    ) -> UpdateQuestionResponse:
        try:
            question = await self.question_repository.get_question_rubric(question_id)
            if question is None:
                return UpdateQuestionResponse(
                    is_success=False,
                    message="Question not found",
                )

            question.update_text_to_evaluate(request.text)
            question.update_concept(request.concept)
            question.update_definition(request.definition)
            question.update_simple_explanation(request.simple_explanation)
            question.update_correct_sample(request.correct_sample)
            question.update_wrong_sample(request.wrong_sample)
            question.common_misconception = request.common_misconception
            question.semantic_keywords = request.semantic_keywords
            question.rubric = [
                QuestionRubricScore(score=r.score, explanation=r.criteria)
                for r in request.rubric
            ]

            await self.question_repository.update_question(question)
            return UpdateQuestionResponse(
                is_success=True,
                message="Question updated successfully",
            )
        except Exception as e:
            return UpdateQuestionResponse(
                is_success=False,
                message=f"Failed to update question: {str(e)}",
            )
