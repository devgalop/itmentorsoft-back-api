from abc import ABC, abstractmethod
from enum import Enum

from itmentorsoft_persistence.dto import (
    AssessmentAnswer,
    Question,
    QualifierResult,
)


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


class ModelExplorerService(ABC):

    @abstractmethod
    async def get_available_models(self) -> list[str]:
        """Fetches the list of available models from the LLM Provider.

        Returns:
            list[str]: A list of model names available for use.
        """
        pass


class AvailableProcesses(Enum):
    QUALIFIER = "qualifier"
    CLASSIFIER = "classifier"


class ModelSelectorService(ABC):
    @abstractmethod
    def get_selected_model(self, process: AvailableProcesses) -> str:
        """Fetches the currently selected model from the LLM Provider.

        Args:
            process (AvailableProcesses): The process for which to get the selected model.

        Returns:
            str: The name of the currently selected model.
        """
        pass

    @abstractmethod
    async def set_selected_model(self, process: AvailableProcesses, model_name: str):
        """Sets the currently selected model in the LLM Provider.

        Args:
            process (AvailableProcesses): The process for which to set the selected model.
            model_name (str): The name of the model to set as selected.
        """
        pass
