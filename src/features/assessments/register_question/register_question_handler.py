from itmentorsoft_persistence import QuestionDifficulty

from src.features.assessments.register_question.register_question_request import (
    RegisterQuestionRequest,
)
from src.features.assessments.register_question.register_question_response import (
    RegisterQuestionResponse,
)
from src.features.assessments.shared.question_manager_service import (
    CreateQuestionRequest,
    QuestionManagerService,
)


class RegisterQuestionHandler:
    def __init__(
        self,
        question_service: QuestionManagerService,
    ):
        self.question_service = question_service

    async def handle(
        self, request: RegisterQuestionRequest, user_name: str
    ) -> RegisterQuestionResponse:
        try:

            if request.difficulty not in [
                difficulty.value for difficulty in QuestionDifficulty
            ]:
                return RegisterQuestionResponse(
                    is_success=False,
                    message=f"Failed to register question: Invalid difficulty '{request.difficulty}'",
                )

            response = await self.question_service.create_question(
                CreateQuestionRequest(model=request, user_name=user_name)
            )

            if not response:
                return RegisterQuestionResponse(
                    is_success=False,
                    message="Failed to register question: Unknown error",
                )

            if not response.is_success:
                return RegisterQuestionResponse(
                    is_success=False,
                    message=f"Failed to register question: {response.message}",
                )

            return RegisterQuestionResponse(
                is_success=response.is_success,
                message=response.message,
                question_id=response.question_id,
            )
        except Exception as e:
            return RegisterQuestionResponse(
                is_success=False, message=f"Failed to register question: {str(e)}"
            )
