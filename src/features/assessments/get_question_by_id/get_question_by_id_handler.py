from src.features.assessments.get_question_by_id.get_question_by_id_request import (
    GetQuestionByIdRequest,
)
from src.features.assessments.get_question_by_id.get_question_by_id_response import (
    GetQuestionByIdResponse,
    QuestionData,
    QuestionRubricScoreData,
)
from itmentorsoft_persistence.repositories import QuestionRepository


class GetQuestionByIdHandler:
    def __init__(self, question_repository: QuestionRepository):
        self.question_repository = question_repository

    async def handle(self, request: GetQuestionByIdRequest) -> GetQuestionByIdResponse:
        try:
            question = await self.question_repository.get_question_rubric(
                request.question_id
            )
            if question is None:
                return GetQuestionByIdResponse(
                    is_success=False,
                    message="Question not found",
                    question=None,
                )

            question_data = QuestionData(
                question_id=question.question_id,
                text=question.text_to_evaluate,
                concept=question.concept,
                definition=question.definition,
                simple_explanation=question.simple_explanation,
                correct_sample=question.correct_sample,
                wrong_sample=question.wrong_sample,
                common_misconception=question.common_misconception,
                rubric=[
                    QuestionRubricScoreData(score=r.score, explanation=r.explanation)
                    for r in question.rubric
                ],
                semantic_keywords=question.semantic_keywords,
                status=question.status.value,
            )
            return GetQuestionByIdResponse(
                is_success=True,
                message="Question retrieved successfully",
                question=question_data,
            )
        except Exception as e:
            return GetQuestionByIdResponse(
                is_success=False,
                message=f"Failed to retrieve question: {str(e)}",
                question=None,
            )
