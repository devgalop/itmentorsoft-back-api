from src.features.assessments.get_quantity_of_assessments.get_quantity_of_assessments_request import (
    GetQuantityOfAssessmentsRequest,
)
from src.features.assessments.get_quantity_of_assessments.get_quantity_of_assessments_response import (
    GetQuantityOfAssessmentsResponse,
)
from itmentorsoft_persistence.repositories import AssessmentRepository


class GetQuantityOfAssessmentsHandler:
    def __init__(self, assessment_repository: AssessmentRepository):
        self.assessment_repository = assessment_repository

    async def handle(
        self, request: GetQuantityOfAssessmentsRequest
    ) -> GetQuantityOfAssessmentsResponse:
        total_assessments = (
            await self.assessment_repository.get_quantity_of_assessments(
                request.student_id
            )
        )
        return GetQuantityOfAssessmentsResponse(
            is_success=True,
            message="Quantity of assessments retrieved successfully.",
            total_assessments=total_assessments,
        )
