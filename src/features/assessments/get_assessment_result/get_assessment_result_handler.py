from src.features.assessments.get_assessment_result.get_assessment_result_request import (
    GetAssessmentResultRequest,
)
from src.features.assessments.get_assessment_result.get_assessment_result_response import (
    AnswerScore,
    GetAssessmentResultResponse,
    StudentAssessmentResult,
)
from itmentorsoft_persistence.repositories import AssessmentRepository


class GetAssessmentResultHandler:
    def __init__(self, assessment_repository: AssessmentRepository):
        self.assessment_repository = assessment_repository

    async def handle(
        self, request: GetAssessmentResultRequest
    ) -> GetAssessmentResultResponse:
        assessment_result = await self.assessment_repository.get_assessment_result(
            request.assessment_id, request.user_id
        )
        if assessment_result is None:
            return GetAssessmentResultResponse(
                is_success=False,
                message="Assessment result not found.",
                result=None,
            )
        result = StudentAssessmentResult(
            assessment_id=assessment_result.assessment_id,
            user_id=assessment_result.student_id,
            avg_score=assessment_result.avg_score,
            classification=assessment_result.classification,
            feedback=assessment_result.feedback,
            answer_scores=[
                AnswerScore(
                    question_id=ans.question_id,
                    question_text=ans.question_text,
                    answer=ans.answer,
                    score=ans.score,
                    feedback=ans.feedback,
                    misconceptions=ans.misconceptions,
                    key_concepts=ans.key_concepts,
                )
                for ans in assessment_result.answer_scores
            ],
        )
        return GetAssessmentResultResponse(
            is_success=True,
            message="Assessment result retrieved successfully.",
            result=result,
        )
