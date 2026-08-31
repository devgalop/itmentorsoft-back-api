from datetime import datetime
from secrets import SystemRandom
import uuid

from src.features.assessments.get_assessment.get_assessment_request import (
    GetAssessmentRequest,
)
from src.features.assessments.get_assessment.get_assessment_response import (
    EvaluativeQuestionData,
    GetAssessmentResponse,
)
from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_request import (
    GetAssessmentByTopicRequest,
)
from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_response import (
    EvaluativeQuestionDataByTopic,
    GetAssessmentByTopicResponse,
)
from src.features.assessments.shared.assessment import AssessmentQuiz
from src.features.assessments.shared.assessment_repository import AssessmentRepository
from src.features.assessments.shared.question import (
    EvaluativeQuestion,
    QuestionDifficulty,
)
from src.features.assessments.shared.question_assessment_repository import (
    QuestionAssessmentRepository,
)
from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants

_rng = SystemRandom()


def _get_number_of_questions() -> int:
    """Get the number of questions to be used in assessments from environment variables.

    Returns:
        int: The number of questions to be used in assessments.

    Raises:
        ValueError: If the ASSESSMENT_MAX_QUESTIONS_NUMBER environment variable is not set or is not a valid integer.
    """
    if EnvironmentVariablesConstants.ASSESSMENT_MAX_QUESTIONS_NUMBER is None:
        raise ValueError(
            "ASSESSMENT_MAX_QUESTIONS_NUMBER environment variable is not set."
        )

    try:
        value = int(EnvironmentVariablesConstants.ASSESSMENT_MAX_QUESTIONS_NUMBER)
    except ValueError:
        raise ValueError(
            f"ASSESSMENT_MAX_QUESTIONS_NUMBER must be a valid integer, got: {EnvironmentVariablesConstants.ASSESSMENT_MAX_QUESTIONS_NUMBER}"
        )

    return value


NUMBER_OF_QUESTIONS = _get_number_of_questions()


class GetRandomQuestionsRequest:
    def __init__(
        self,
        number_of_questions: int,
        difficulty_level: QuestionDifficulty,
    ):
        self.number_of_questions = number_of_questions
        self.difficulty_level = difficulty_level


class GetRandomQuestionsByTopicRequest(GetRandomQuestionsRequest):
    def __init__(
        self,
        number_of_questions: int,
        difficulty_level: QuestionDifficulty,
        topic_id: str,
    ):
        super().__init__(number_of_questions, difficulty_level)
        self.topic_id = topic_id


class GetAssessmentService:
    def __init__(
        self,
        question_repository: QuestionAssessmentRepository,
        assessment_repository: AssessmentRepository,
    ):
        self.question_repository = question_repository
        self.assessment_repository = assessment_repository

    async def generate_assessment(
        self, request: GetAssessmentRequest
    ) -> GetAssessmentResponse:
        """Generate dynamically assessment questions based on the student's level and the number of questions requested.
        When the assessment is for an initial evaluation, questions are distributed evenly across all difficulty levels.
        For follow-up evaluations, 60% of the questions are selected from the student's current level, while the remaining 40% are distributed among adjacent levels.

        Args:
            request (GetAssessmentRequest): An object containing the student's ID and the number of questions to generate.

        Returns:
            GetAssessmentResponse: An object containing the generated assessment questions.
        """
        questions: list[EvaluativeQuestionData] = []
        # Se debe implementar la lógica para calcular el numero de preguntas dependiendo del tipo de evaluación (inicial o seguimiento) y el nivel del estudiante
        number_of_questions_base: int = NUMBER_OF_QUESTIONS // len(QuestionDifficulty)
        remaining_questions: int = NUMBER_OF_QUESTIONS % len(QuestionDifficulty)

        for index, difficulty in enumerate(QuestionDifficulty):
            total_questions = number_of_questions_base + (
                1 if index < remaining_questions else 0
            )
            questions += await self.get_random_questions(
                GetRandomQuestionsRequest(
                    number_of_questions=total_questions, difficulty_level=difficulty
                )
            )

        assessment_id = uuid.uuid4().hex

        await self.assessment_repository.save_assessment(
            AssessmentQuiz(
                assessment_id=assessment_id,
                user_id=request.student_id,
                created_at=datetime.now(),
                questions=[question.question_id for question in questions],
            )
        )

        return GetAssessmentResponse(
            is_success=True,
            message="Assessment retrieved successfully",
            assessment_id=assessment_id,
            questions=questions,
        )

    async def is_initial_assessment(self, student_id: str) -> bool:
        """Determine if the assessment being generated is the student's initial assessment by checking if the student has taken any previous assessments.

        Args:
            student_id (str): The ID of the student to check.

        Returns:
            bool: True if the assessment is the student's initial assessment, False otherwise.
        """
        return not await self.assessment_repository.has_first_assessment(student_id)

    async def get_random_questions(
        self, request: GetRandomQuestionsRequest
    ) -> list[EvaluativeQuestionData]:
        """Obtain a random selection of questions based on the specified difficulty level and number of questions.

        Args:
            request (GetRandomQuestionsRequest): An object containing the number of questions to retrieve and the desired difficulty level.

        Returns:
            list[EvaluativeQuestionData]: A list of evaluative question data objects representing the randomly selected questions.
        """
        questions = await self.question_repository.get_question_by_level(
            difficulty=request.difficulty_level
        )

        # If the number of questions requested exceeds the available questions, adjust the number to the maximum available.
        if request.number_of_questions > len(questions):
            request.number_of_questions = len(questions)

        questions_selected: list[EvaluativeQuestion] = _rng.sample(
            questions, request.number_of_questions
        )
        return [
            EvaluativeQuestionData(
                question_id=question.question_id,
                text_to_evaluate=question.text_to_evaluate,
            )
            for question in questions_selected
        ]

    async def generate_assessment_by_topic(
        self, request: GetAssessmentByTopicRequest
    ) -> GetAssessmentByTopicResponse:
        """Generate dynamically assessment questions based on the student's level and the number of questions requested.
        When the assessment is for an initial evaluation, questions are distributed evenly across all difficulty levels.
        For follow-up evaluations, 60% of the questions are selected from the student's current level, while the remaining 40% are distributed among adjacent levels.

        Args:
            request (GetAssessmentByTopicRequest): An object containing the student's ID, the topic ID and the number of questions to generate.
        Returns:
            GetAssessmentByTopicResponse: An object containing the generated assessment questions.
        """
        questions: list[EvaluativeQuestionDataByTopic] = []
        # Se debe implementar la lógica para calcular el numero de preguntas dependiendo del tipo de evaluación (inicial o seguimiento) y el nivel del estudiante
        number_of_questions_base: int = NUMBER_OF_QUESTIONS // len(QuestionDifficulty)
        remaining_questions: int = NUMBER_OF_QUESTIONS % len(QuestionDifficulty)

        for index, difficulty in enumerate(QuestionDifficulty):
            total_questions = number_of_questions_base + (
                1 if index < remaining_questions else 0
            )
            questions += await self.get_random_questions_by_topic(
                GetRandomQuestionsByTopicRequest(
                    number_of_questions=total_questions,
                    difficulty_level=difficulty,
                    topic_id=request.topic_id,
                )
            )

        assessment_id = uuid.uuid4().hex

        await self.assessment_repository.save_assessment(
            AssessmentQuiz(
                assessment_id=assessment_id,
                user_id=request.student_id,
                created_at=datetime.now(),
                questions=[question.question_id for question in questions],
            )
        )

        return GetAssessmentByTopicResponse(
            is_success=True,
            message="Assessment retrieved successfully",
            assessment_id=assessment_id,
            topic_id=request.topic_id,
            questions=questions,
        )

    async def get_random_questions_by_topic(
        self, request: GetRandomQuestionsByTopicRequest
    ) -> list[EvaluativeQuestionDataByTopic]:
        """Obtain a random selection of questions based on the specified difficulty level, topic ID and number of questions.

        Args:
            request (GetRandomQuestionsByTopicRequest): An object containing the number of questions to retrieve, the desired difficulty level and the topic ID.
        Returns:
            list[EvaluativeQuestionDataByTopic]: A list of evaluative question data objects representing the randomly selected questions.
        """
        questions = await self.question_repository.get_questions_by_topic(
            topic=request.topic_id, difficulty=request.difficulty_level
        )

        # If the number of questions requested exceeds the available questions, adjust the number to the maximum available.
        if request.number_of_questions > len(questions):
            request.number_of_questions = len(questions)

        questions_selected: list[EvaluativeQuestion] = _rng.sample(
            questions, request.number_of_questions
        )
        return [
            EvaluativeQuestionDataByTopic(
                question_id=question.question_id,
                topic=question.topic,
                text_to_evaluate=question.text_to_evaluate,
            )
            for question in questions_selected
        ]
