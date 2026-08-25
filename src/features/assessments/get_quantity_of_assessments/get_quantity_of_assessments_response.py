from pydantic import BaseModel


class GetQuantityOfAssessmentsResponse(BaseModel):
    is_success: bool
    message: str
    total_assessments: int
