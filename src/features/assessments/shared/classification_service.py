from abc import ABC, abstractmethod
import json
from itmentorsoft_persistence.dto import ClassificationResult


class QuestionAnswerQualification:
    def __init__(
        self,
        question_id: str,
        user_id: str,
        assessment_id: str,
        question_difficulty: str,
        answer: str,
        score: int,
        feedback: str,
        key_concepts_detected: list[str],
        misconceptions_detected: list[str],
    ):
        self.question_id = question_id
        self.user_id = user_id
        self.assessment_id = assessment_id
        self.question_difficulty = question_difficulty
        self.answer = answer
        self.score = score
        self.feedback = feedback
        self.key_concepts_detected = key_concepts_detected or []
        self.misconceptions_detected = misconceptions_detected or []

    def to_text(self) -> str:
        """Convert the question answer qualification to a text representation.

        Returns:
            str: The text representation of the question answer qualification.
        """
        return json.dumps(
            {
                "question_id": self.question_id,
                "user_id": self.user_id,
                "assessment_id": self.assessment_id,
                "question_difficulty": self.question_difficulty,
                "answer": self.answer,
                "score": self.score,
                "feedback": self.feedback,
                "key_concepts_detected": self.key_concepts_detected,
                "misconceptions_detected": self.misconceptions_detected,
            }
        )


class ClassificationPrompt:
    def __init__(self, qualifications: list[QuestionAnswerQualification]):
        self.qualifications = qualifications


class ClassificationError(Exception):
    def __init__(
        self,
        raw_response: str,
        message: str = "Failed to parse batch qualification response",
    ):
        self.raw_response = raw_response
        super().__init__(message)


class ClassificationService(ABC):
    @abstractmethod
    async def classify(self, input_data: ClassificationPrompt) -> ClassificationResult:
        """Classify the user's knowledge based on their answer to a question.

        Args:
            input_data (ClassificationPrompt): The prompt containing the question answer qualifications and other relevant information.

        Returns:
            ClassificationResult: The result of the classification, including the classification and feedback.
        """
        pass
