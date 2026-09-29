from itmentorsoft_persistence import QuestionDetails
from pydantic import BaseModel


class GetAllQuestionVersionsResponse(BaseModel):
    is_success: bool
    message: str
    questions: list[QuestionDetails] = []
    total: int = 0
