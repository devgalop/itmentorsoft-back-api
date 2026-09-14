from itmentorsoft_persistence.repositories import QuestionRepository
from src.features.assessments.register_question.register_question_request import (
    QuestionRubric,
    RegisterQuestionRequest,
)
from src.features.assessments.shared.question_manager_service import (
    CreateQuestionRequest,
    QuestionManagerService,
)
from src.features.assessments.update_question.update_question_request import (
    UpdateQuestionRequest,
)
from src.features.assessments.update_question.update_question_response import (
    UpdateQuestionResponse,
)


class UpdateQuestionHandler:
    def __init__(
        self,
        question_manager_service: QuestionManagerService,
        question_repository: QuestionRepository,
    ):
        self.question_manager_service = question_manager_service
        self.question_repository = question_repository

    async def handle(
        self, question_id: str, request: UpdateQuestionRequest, user_name: str
    ) -> UpdateQuestionResponse:
        try:
            question = await self.question_repository.get_question_rubric(question_id)
            if question is None:
                return UpdateQuestionResponse(
                    is_success=False,
                    message="Question not found",
                )

            await self.question_manager_service.update_question(question)

            new_version = question.version + 1
            creation_request = RegisterQuestionRequest(
                text=request.text,
                concept=request.concept,
                definition=request.definition,
                simple_explanation=request.simple_explanation,
                correct_sample=request.correct_sample,
                wrong_sample=request.wrong_sample,
                common_misconception=request.common_misconception,
                semantic_keywords=request.semantic_keywords,
                rubric=[
                    QuestionRubric(score=r.score, criteria=r.criteria)
                    for r in request.rubric
                ],
                version=new_version,
            )

            await self.question_manager_service.create_question(
                CreateQuestionRequest(model=creation_request, user_name=user_name)
            )

            return UpdateQuestionResponse(
                is_success=True,
                message="Question updated successfully",
            )
        except Exception as e:
            return UpdateQuestionResponse(
                is_success=False,
                message=f"Failed to update question: {str(e)}",
            )
