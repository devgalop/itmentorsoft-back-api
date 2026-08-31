from datetime import datetime
from typing import Type
from pydantic import BaseModel
from src.features.assessments.register_question.register_question_request import (
    RegisterQuestionRequest,
)
from src.features.assessments.shared.question import (
    Question,
    QuestionBuilder,
    QuestionRubricScore,
)
from src.features.assessments.shared.questions_repository import QuestionRepository
from src.features.shared.notification_service import (
    NotificationConfigBuilder,
    NotificationService,
)
from src.features.shared.template_loader import TemplateLoader
from src.features.user_management.shared.user_repository import UserRepository
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
                .build()
            )
            await self.question_repository.save_question(question)

            admin_users = await self.user_repository.get_admin_users()
            if not admin_users:
                print("No admin users found to notify.")
                return CreateQuestionResponse(
                    is_success=True,
                    message="Question was created successfully, but no admin users found to notify.",
                    question_id=question.question_id,
                )

            html_content = self.template_loader.load("item_created")
            for admin_user in admin_users:
                notification_config_builder = NotificationConfigBuilder(
                    admin_user.email, "New Question Registered"
                )

                final_html_content = (
                    html_content.replace("%REVIEWER%", admin_user.username)
                    .replace("%CREATED_BY%", request.user_name)
                    .replace("%OBJECT_NAME%", "Pregunta + rubrica de evaluación")
                    .replace("%OBJECT_CODE%", question.question_id)
                    .replace("%CREATED_DATE%", datetime.now().strftime("%Y-%m-%d"))
                    .replace(
                        "%URL_REVIEW%",
                        f"{EnvironmentVariablesConstants.REVIEW_URL_BASE}?page=0&page_size=10",
                    )
                )

                notification_config_builder.set_template(final_html_content)
                notification_config = notification_config_builder.build()

                _ = await self.notification_service.send_notification(
                    notification_config
                )

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
