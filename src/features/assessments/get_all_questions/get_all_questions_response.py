from pydantic import BaseModel

from itmentorsoft_persistence.dto import QuestionDetails


class GetAllQuestionsResponse(BaseModel):
    is_success: bool
    message: str
    questions: list[QuestionDetails] = []
    total: int = 0
