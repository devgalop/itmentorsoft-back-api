from abc import ABC, abstractmethod

from src.features.assessments.shared.assessment import AssessmentAnswer
from src.features.assessments.shared.question import Question


class QualifierPrompt:
    def __init__(
        self,
        rubric: Question,
        qualifier_mode: str,
        user_id: str,
        user_answer: str,
        assessment_id: str,
        answer_id: str,
    ):
        self.rubric = rubric
        self.qualifier_mode = qualifier_mode
        self.user_id = user_id
        self.user_answer = user_answer
        self.assessment_id = assessment_id
        self.answer_id = answer_id


class BatchQualifierPrompt:
    """Prompt for batch qualification of multiple answers in a single LLM call."""

    def __init__(
        self,
        rubrics: list[Question],
        answers: list[AssessmentAnswer],
        qualifier_mode: str,
        user_id: str,
        assessment_id: str,
    ):
        if len(rubrics) != len(answers):
            raise ValueError(
                f"BatchQualifierPrompt expects the same number of rubrics and answers, got {len(rubrics)} rubrics and {len(answers)} answers"
            )
        self.rubrics = rubrics
        self.answers = answers
        self.qualifier_mode = qualifier_mode
        self.user_id = user_id
        self.assessment_id = assessment_id


class BatchQualificationError(Exception):
    """Raised when a batch LLM response cannot be parsed as a valid JSON array."""

    def __init__(
        self,
        raw_response: str,
        message: str = "Failed to parse batch qualification response",
    ):
        self.raw_response = raw_response
        super().__init__(message)


class QualifierResult:
    def __init__(
        self,
        id: str,
        question_id: str,
        user_id: str,
        score: int,
        feedback: str,
        key_concepts_detected: list[str],
        misconceptions_detected: list[str],
        question_topic: str,
        assessment_id: str,
        question_difficulty: str,
        answer_id: str,
    ):
        self.id = id
        self.question_id = question_id
        self.user_id = user_id
        self.score = score
        self.feedback = feedback
        self.key_concepts_detected = key_concepts_detected or []
        self.misconceptions_detected = misconceptions_detected or []
        self.question_topic = question_topic
        self.assessment_id = assessment_id
        self.question_difficulty = question_difficulty
        self.answer_id = answer_id


class TopicResult:
    def __init__(self, user_id: str, topic: str, score: int):
        self.user_id = user_id
        self.topic = topic
        self.score = score


class QualifierService(ABC):

    @abstractmethod
    async def qualify(self, qualifier_prompt: QualifierPrompt) -> QualifierResult:
        """Assign a score based on the user's answer to a question, and provide feedback.

        Args:
            qualifier_prompt (QualifierPrompt): The prompt containing the question, user answer, and qualifier mode.

        Returns:
            QualifierResult: The result of the qualification, including score, feedback, key concepts detected, and misconceptions detected.
        """
        pass

    @abstractmethod
    async def qualify_batch(
        self, batch_prompt: BatchQualifierPrompt
    ) -> list[QualifierResult]:
        """Evaluate multiple answers in a single LLM call.

        Returns QualifierResult list in the same order as batch_prompt.answers.
        Raises BatchQualificationError if response cannot be parsed.
        """
        pass


class QualifierModelsService(ABC):
    @abstractmethod
    async def get_available_models(self) -> list[str]:
        """Fetches the list of available models from the LLM Provider.

        Returns:
            list[str]: A list of model names available for use.
        """
        pass
