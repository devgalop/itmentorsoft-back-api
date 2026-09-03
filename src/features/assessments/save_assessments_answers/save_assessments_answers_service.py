from datetime import datetime
import uuid

from src.features.assessments.evaluate.evaluate_assessment_service import (
    EvaluateAssessmentService,
)
from src.features.assessments.evaluate.evaluate_message import EvaluateMessage
from src.features.assessments.save_assessments_answers.save_assessments_answers_request import (
    SaveAssessmentsAnswersRequest,
)
from src.features.assessments.save_assessments_answers.save_assessments_answers_response import (
    SaveAssessmentsAnswersResponse,
)
from itmentorsoft_persistence.dto import (
    Assessment,
    AssessmentAnswer,
    AssessmentQuiz,
)
from itmentorsoft_persistence.repositories import AssessmentRepository
from src.features.shared.publisher_service import PublisherService
from itmentorsoft_persistence.repositories import UserRepository


class SaveAssessmentsAnswersService:
    def __init__(
        self,
        assessment_repository: AssessmentRepository,
        user_repository: UserRepository,
        evaluator_service: EvaluateAssessmentService,
        publisher_service: PublisherService,
    ):
        self.assessment_repository = assessment_repository
        self.user_repository = user_repository
        self.evaluator_service = evaluator_service
        self.publisher_service = publisher_service

    async def save_assessment_answers(
        self, request: SaveAssessmentsAnswersRequest
    ) -> SaveAssessmentsAnswersResponse:
        """Validate and save the answers of an assessment

        Args:
            request (SaveAssessmentsAnswersRequest): Assessment answers to be saved

        Returns:
            SaveAssessmentsAnswersResponse: The result of the operation
        """
        try:
            if not await self.is_existing_user(request.user_id):
                return SaveAssessmentsAnswersResponse(
                    is_success=False, message="User not found."
                )

            assessment_quiz = await self.get_assessment_quiz(request.assessment_id)

            if not assessment_quiz:
                return SaveAssessmentsAnswersResponse(
                    is_success=False,
                    message="Assessment quiz not found for the given assessment ID.",
                )

            existing_assessment = await self.assessment_repository.get_assessment(
                request.assessment_id
            )

            if existing_assessment and len(existing_assessment.answers) > 0:
                return SaveAssessmentsAnswersResponse(
                    is_success=False,
                    message="Assessment answers already exist for the given assessment ID.",
                )

            if not self.is_assessment_assign_to_user(assessment_quiz, request.user_id):
                return SaveAssessmentsAnswersResponse(
                    is_success=False,
                    message="The assessment quiz does not belong to the user.",
                )

            questions = assessment_quiz.questions if assessment_quiz else []
            answered_question_ids = [answer.question_id for answer in request.answers]

            if not self.are_answered_questions_valid(answered_question_ids, questions):
                return SaveAssessmentsAnswersResponse(
                    is_success=False,
                    message="Invalid answered question IDs. They must match the questions of the assessment quiz.",
                )

            assessment = self.create_assessment_model(request)

            await self.assessment_repository.save_assessment_answers(assessment)

            await self.publisher_service.publish(request=EvaluateMessage(assessment))

            return SaveAssessmentsAnswersResponse(
                is_success=True, message="Assessment answers saved successfully."
            )
        except Exception as e:
            return SaveAssessmentsAnswersResponse(
                is_success=False, message=f"An error occurred: {str(e)}"
            )

    async def is_existing_user(self, user_id: str) -> bool:
        """Check if a user exists by their ID

        Args:
            user_id (str): The ID of the user to check.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        user = await self.user_repository.get_user_by_id(user_id)
        return user is not None

    async def get_assessment_quiz(self, assessment_id: str) -> AssessmentQuiz | None:
        """Obtain an assessment quiz by Id

        Args:
            assessment_id (str): The ID of the assessment quiz to retrieve.

        Returns:
            The assessment quiz corresponding to the given ID, or None if not found.
        """
        return await self.assessment_repository.get_assessment_quiz(assessment_id)

    def is_assessment_assign_to_user(
        self, assessment: AssessmentQuiz, user_id: str
    ) -> bool:
        """Check if an assessment quiz is assigned to a user

        Args:
            assessment (AssessmentQuiz): The assessment quiz to check.
            user_id (str): The ID of the user to check against.

        Returns:
            bool: True if the assessment quiz is assigned to the user, False otherwise.
        """
        return assessment.user_id == user_id

    def are_answered_questions_valid(
        self, answered_question_ids: list[str], questions: list[str]
    ) -> bool:
        """Check if the answered question IDs are valid for the given questions

        Args:
            answered_question_ids (list[str]): The list of answered question IDs to validate.
            questions (list[str]): The list of valid question IDs for the assessment quiz.

        Returns:
            bool: True if the answered question IDs are valid, False otherwise.
        """
        if not questions:
            return False

        if len(answered_question_ids) != len(set(answered_question_ids)):
            return False

        if set(answered_question_ids) != set(questions):
            return False
        return True

    def create_assessment_model(
        self, request: SaveAssessmentsAnswersRequest
    ) -> Assessment:
        """Create an Assessment model from the given request

        Args:
            request (SaveAssessmentsAnswersRequest): The request containing the assessment answers data.

        Returns:
            Assessment: The created Assessment model.
        """
        answers: list[AssessmentAnswer] = []
        for answer in request.answers:
            answers.append(
                AssessmentAnswer(
                    answer_id=uuid.uuid4().hex,
                    assessment_id=request.assessment_id,
                    question_id=answer.question_id,
                    answer=answer.answer,
                    time_taken_seconds=answer.takes_time_seconds,
                )
            )

        assessment = Assessment(
            assessment_id=request.assessment_id,
            user_id=request.user_id,
            created_at=datetime.now(),
            answers=answers,
        )
        return assessment
