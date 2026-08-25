from pydantic import BaseModel


class AssessmentSummary(BaseModel):
    assessment_id: str
    score: float
    date_taken: str
    classification: str | None = None
    feedback: str | None = None


class GetAssessmentsSummaryResponse(BaseModel):
    is_success: bool
    message: str
    total_assessments: int
    assessments: list[AssessmentSummary]
