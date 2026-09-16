from datetime import datetime
from typing import Type
from itmentorsoft_persistence import QuestionDifficulty, QuestionStatus
from pydantic import BaseModel
from src.features.assessments.register_question.register_question_request import (
    RegisterQuestionRequest,
)
from itmentorsoft_persistence.dto import (
    Question,
    QuestionBuilder,
    QuestionRubricScore,
)
from itmentorsoft_persistence.repositories import QuestionRepository, UserRepository
from src.features.shared.notification_service import (
    NotificationConfigBuilder,
    NotificationService,
)
from src.features.shared.template_loader import TemplateLoader
from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants


class CreateQuestionRequest(BaseModel):
    model: RegisterQuestionRequest
    user_name: str


class CreateQuestionResponse(BaseModel):
    is_success: bool
    message: str = ""
    question_id: str = ""


class QuestionManagerService:
    def __init__(
        self,
        question_repository: QuestionRepository,
        question_builder: Type[QuestionBuilder],
        notification_service: NotificationService,
        template_loader: TemplateLoader,
        user_repository: UserRepository,
    ):
        self.question_repository = question_repository
        self.question_builder = question_builder
        self.notification_service = notification_service
        self.template_loader = template_loader
        self.user_repository = user_repository

    async def create_question(
        self, request: CreateQuestionRequest
    ) -> CreateQuestionResponse:
        """Create a new question based on the provided request.

        Args:
            request (CreateQuestionRequest): The request object containing the question details and the user name.

        Returns:
            CreateQuestionResponse: The response object indicating the success or failure of the question creation.
        """
        try:
            rubric_scores: list[QuestionRubricScore] = [
                QuestionRubricScore(score=r.score, explanation=r.criteria)
                for r in request.model.rubric
            ]
            difficulty = QuestionDifficulty.EASY
            if request.model.difficulty:
                difficulty = QuestionDifficulty(request.model.difficulty)
            question: Question = (
                self.question_builder()
                .set_text_to_evaluate(request.model.text)
                .set_concept(request.model.concept)
                .set_definition(request.model.definition)
                .set_simple_explanation(request.model.simple_explanation)
                .set_correct_sample(request.model.correct_sample)
                .set_wrong_sample(request.model.wrong_sample)
                .add_common_misconceptions(request.model.common_misconception)
                .add_semantic_keywords(request.model.semantic_keywords)
                .add_rubrics(rubric_scores)
                .set_version(request.model.version)
                .set_classification(request.model.topic)
                .set_difficulty(difficulty)
                .build()
            )
            await self.question_repository.save_question(question)

            is_sent = await self.send_item_created_notification(
                question, request.user_name
            )
            if not is_sent:
                print("Failed to send item created notifications.")

            return CreateQuestionResponse(
                is_success=True,
                message="Question created successfully",
                question_id=question.question_id,
            )
        except Exception as e:
            print(f"Error creating question: {e}")
            return CreateQuestionResponse(
                is_success=False, message="Error creating question"
            )

    async def update_question(self, question: Question):
        """Archived the previous version of the question before updating it.

        Args:
            question (Question): The question object to be archived.
        """
        question.update_status(QuestionStatus.ARCHIVED)
        await self.question_repository.update_question(question)

    async def send_item_created_notification(
        self, question: Question, author_user_name: str
    ) -> bool:
        """
        Sends a notification to all admin users when a new question is created.

        Args:
            question (Question): The question object that was created.
            author_user_name (str): The username of the author who created the question.

        Returns:
            bool: True if the notification was sent successfully, False otherwise.
        """
        SUBJECT = "New Question Registered"
        OBJECT_NAME = "Pregunta + rubrica de evaluación"
        admin_users = await self.user_repository.get_admin_users()
        if not admin_users:
            print("No admin users found to notify.")
            return False
        html_content = self.template_loader.load("item_created")
        for admin_user in admin_users:
            notification_config_builder = NotificationConfigBuilder(
                admin_user.email, SUBJECT
            )

            final_html_content = (
                html_content.replace("%REVIEWER%", admin_user.username)
                .replace("%CREATED_BY%", author_user_name)
                .replace("%OBJECT_NAME%", OBJECT_NAME)
                .replace("%OBJECT_CODE%", f"{question.question_id}-v{question.version}")
                .replace("%CREATED_DATE%", datetime.now().strftime("%Y-%m-%d"))
                .replace(
                    "%URL_REVIEW%",
                    f"{EnvironmentVariablesConstants.REVIEW_URL_BASE}?page=0&page_size=10",
                )
            )

            notification_config_builder.set_template(final_html_content)
            notification_config = notification_config_builder.build()

            _ = await self.notification_service.send_notification(notification_config)
        return True
