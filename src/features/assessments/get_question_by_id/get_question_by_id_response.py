from pydantic import BaseModel


class QuestionRubricScoreData(BaseModel):
    score: int
    explanation: str


class QuestionData(BaseModel):
    question_id: str
    text: str
    concept: str
    definition: str
    simple_explanation: str
    correct_sample: str
    wrong_sample: str
    common_misconception: list[str]
    rubric: list[QuestionRubricScoreData]
    semantic_keywords: list[str]
    status: str
    difficulty: str
    topic: str


class GetQuestionByIdResponse(BaseModel):
    is_success: bool
    message: str
    question: QuestionData | None = None
