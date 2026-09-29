from itmentorsoft_persistence import Question, QuestionDifficulty
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

            if request.difficulty not in [
                difficulty.value for difficulty in QuestionDifficulty
            ]:
                return UpdateQuestionResponse(
                    is_success=False,
                    message=f"Failed to update question: Invalid difficulty '{request.difficulty}'",
                )

            previous_question = await self.question_repository.get_question_rubric(
                question_id
            )
            if previous_question is None:
                return UpdateQuestionResponse(
                    is_success=False,
                    message="Question not found",
                )

            await self.question_manager_service.update_question(previous_question)

            ## Se debe detectar si es la root question y enviar los parametros
            previous_version_id = self.get_previous_version_id(previous_question)
            root_version_id = self.get_root_version_id(previous_question)

            new_version = previous_question.version + 1
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
                difficulty=request.difficulty,
                topic=request.topic,
                previous_version_id=previous_version_id,
                root_version_id=root_version_id,
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

    def is_root_question(self, question: Question) -> bool:
        return question.root_version_id is None or question.root_version_id == ""

    def get_root_version_id(self, question: Question) -> str:
        if self.is_root_question(question):
            return question.question_id
        return question.root_version_id

    def get_previous_version_id(self, question: Question) -> str:
        return question.question_id
