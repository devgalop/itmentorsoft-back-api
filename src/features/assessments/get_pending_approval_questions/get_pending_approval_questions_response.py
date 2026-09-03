from pydantic import BaseModel

from itmentorsoft_persistence.dto import QuestionDetails


class GetPendingApprovalQuestionsResponse(BaseModel):
    is_success: bool
    message: str
    questions: list[QuestionDetails] = []
    total: int = 0
