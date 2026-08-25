from abc import ABC, abstractmethod

from src.features.assessments.shared.assessment import (
    Assessment,
    AssessmentQuiz,
    PaginatedAssessmentSummary,
)
from src.features.assessments.shared.classification_service import ClassificationResult
from src.features.assessments.shared.qualifier_service import (
    QualifierResult,
    TopicResult,
)
from src.features.reports.shared.student_report import (
    StudentAssessmentResult,
    StudentProgress,
    StudentSummary,
)


class AssessmentRepository(ABC):

    @abstractmethod
    async def save_assessment(self, assessment: AssessmentQuiz):
        """Save an assessment

        Args:
            assessment: The assessment to be saved.
        """
        pass

    @abstractmethod
    async def save_assessment_answers(self, assessment: Assessment):
        """Save the answers of an assessment

        Args:
            assessment: The assessment with the answers to be saved.
        """
        pass

    @abstractmethod
    async def get_assessment(self, assessment_id: str) -> Assessment | None:
        """Obtain an assessment by Id

        Args:
            assessment_id (str): The ID of the assessment to retrieve.

        Returns:
            The assessment corresponding to the given ID, or None if not found.
        """
        pass

    @abstractmethod
    async def has_first_assessment(self, user_id: str) -> bool:
        """Check if the user has taken their first assessment

        Args:
            user_id (str): The ID of the user to check.
        Returns:
            True if the user has taken their first assessment, False otherwise.
        """
        pass

    @abstractmethod
    async def get_questions_per_quiz(self, assessment_id: str) -> list[str]:
        """Obtain the questions of an assessment quiz by Id

        Args:
            assessment_id (str): The ID of the assessment quiz to retrieve the questions from.

        Returns:
            A list of question IDs corresponding to the given assessment quiz ID.
        """
        pass

    @abstractmethod
    async def get_assessment_quiz(self, assessment_id: str) -> AssessmentQuiz | None:
        """Obtain an assessment quiz by Id

        Args:
            assessment_id (str): The ID of the assessment quiz to retrieve.

        Returns:
            The assessment quiz corresponding to the given ID, or None if not found.
        """
        pass

    @abstractmethod
    async def save_assessment_qualification(self, qualifier_result: QualifierResult):
        """Save the qualification result of an assessment

        Args:
            qualifier_result (QualifierResult): The result of the qualification to be saved.
        """
        pass

    @abstractmethod
    async def save_topic_result(self, topic_result: TopicResult):
        """Save the topic result of an assessment

        Args:
            topic_result (TopicResult): The result of the topic to be saved.
        """
        pass

    @abstractmethod
    async def get_knowledge_profile(self, user_id: str) -> list[TopicResult]:
        """Obtain the knowledge profile of a user

        Args:
            user_id (str): The ID of the user to retrieve the knowledge profile for.

        Returns:
            A list of TopicResult corresponding to the given user ID.
        """
        pass

    @abstractmethod
    async def get_student_summary(self, user_id: str) -> StudentSummary:
        """Obtain the student summary by user ID

        Args:
            user_id (str): The ID of the user to retrieve the student summary for.

        Returns:
            StudentSummary: The student summary corresponding to the given user ID.
        """
        pass

    @abstractmethod
    async def get_student_progress(self, user_id: str) -> StudentProgress | None:
        """Obtain the student progress by user ID

        Args:
            user_id (str): The ID of the user to retrieve the student progress for.

        Returns:
            StudentProgress | None: The student progress corresponding to the given user ID.
        """
        pass

    @abstractmethod
    async def save_classification_result(
        self, classification_result: ClassificationResult
    ):
        """Save the classification result of an assessment

        Args:
            classification_result (ClassificationResult): The result of the classification to be saved.
        """
        pass

    @abstractmethod
    async def get_assessment_result(
        self, assessment_id: str, user_id: str
    ) -> StudentAssessmentResult | None:
        """Obtain the assessment result of an assessment by assessment ID and user ID

        Args:
            assessment_id (str): The ID of the assessment to retrieve the assessment result for.
            user_id (str): The ID of the user to retrieve the assessment result for.

        Returns:
            StudentAssessmentResult | None: The assessment result corresponding to the given assessment ID and user ID, or None if not found.
        """
        pass

    @abstractmethod
    async def is_qualification_completed(
        self, user_id: str, assessment_id: str
    ) -> bool:
        """Check if the qualification process is completed for a user

        Args:
            user_id (str): The ID of the user to check.
            assessment_id (str): The ID of the assessment to check.

        Returns:
            bool: True if the qualification process is completed for the user and assessment, False otherwise.
        """
        pass

    @abstractmethod
    async def get_quantity_of_assessments(self, student_id: str) -> int:
        """Obtain the quantity of assessments for a student by student ID

        Args:
            student_id (str): The ID of the student to retrieve the quantity of assessments for.

        Returns:
            int: The quantity of assessments corresponding to the given student ID.
        """
        pass

    @abstractmethod
    async def get_assessments_summary(
        self, student_id: str, page: int, page_size: int
    ) -> PaginatedAssessmentSummary:
        """Obtain a paginated summary of assessments for a student by student ID

        Args:
            student_id (str): The ID of the student to retrieve the assessment summaries for.
            page (int): The page number to retrieve.
            page_size (int): The number of assessment summaries per page.
        Returns:
            PaginatedAssessmentSummary: A paginated summary of assessments corresponding to the given student ID.
        """
        pass
