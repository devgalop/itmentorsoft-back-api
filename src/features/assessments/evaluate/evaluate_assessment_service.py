import logging
import time
from collections import defaultdict

from itmentorsoft_persistence.dto import Assessment, TopicResult
from src.features.assessments.shared.classification_service import (
    ClassificationPrompt,
    ClassificationService,
    ClassificationResult,
    QuestionAnswerQualification,
)
from src.features.assessments.shared.qualifier_service import (
    QualifierResult,
    AvailableProcesses,
    BatchQualificationError,
    BatchQualifierPrompt,
    ModelExplorerService,
    ModelSelectorService,
    QualifierPrompt,
    QualifierService,
)
from itmentorsoft_persistence.repositories import (
    QuestionRepository,
    AssessmentRepository,
)
from src.infrastructure.classifier.opencode_classifier_service import (
    OpenCodeClassificationService,
)
from itmentorsoft_persistence.mappers import (
    PostgresAssessmentMapper,
    PostgresQuestionMapper,
)

from src.infrastructure.database.postgresql.repository.postgres_assessment_repository import (
    PostgresAssessmentRepository,
)
from src.infrastructure.database.postgresql.repository.postgres_questions_repository import (
    PostgresQuestionsRepository,
)
from itmentorsoft_persistence import (
    AsyncSessionLocal,
)
from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants
from src.infrastructure.model_manager.opencode_model_manager_proxy import (
    OpencodeModelsManagerProxy,
)
from src.infrastructure.qualifier.opencode_qualifier_service import (
    OpencodeQualifierService,
)

logger = logging.getLogger(__name__)


def _validate_chunk_size(raw_value: str | None) -> int:
    """Validate and return the chunk size from an environment variable value.

    Args:
        raw_value: The raw string value from the environment variable, or None.

    Returns:
        The validated chunk size as a positive integer.

    Raises:
        ValueError: If the value is not a positive integer.
    """
    if raw_value is None:
        return 10
    try:
        value = int(raw_value)
        if value <= 0:
            raise ValueError
        return value
    except ValueError:
        raise ValueError(
            f"ASSESSMENT_QUALIFICATION_CHUNK_SIZE must be a positive integer, got: {raw_value}"
        )


ASSESSMENT_QUALIFICATION_CHUNK_SIZE = _validate_chunk_size(
    EnvironmentVariablesConstants.ASSESSMENT_QUALIFICATION_CHUNK_SIZE
)


class EvaluateAssessmentService:
    def __init__(self):
        self.chunk_size = ASSESSMENT_QUALIFICATION_CHUNK_SIZE
        self.assessment_repository: AssessmentRepository | None = None
        self.question_repository: QuestionRepository | None = None
        self.qualifier_service: QualifierService | None = None
        self.classification_service: ClassificationService | None = None
        self.model_selector_service: ModelSelectorService | None = None
        self.model_explorer_service: ModelExplorerService | None = None

    async def evaluate_answers(
        self, assessment: Assessment
    ) -> list[QuestionAnswerQualification]:
        async with AsyncSessionLocal() as session:
            self.assessment_repository = PostgresAssessmentRepository(
                session, PostgresAssessmentMapper
            )
            self.question_repository = PostgresQuestionsRepository(
                session, PostgresQuestionMapper
            )

            self.model_selector_service = OpencodeModelsManagerProxy()
            self.model_explorer_service = OpencodeModelsManagerProxy()

            qualifier_model = self.model_selector_service.get_selected_model(
                AvailableProcesses.QUALIFIER
            )
            classifier_model = self.model_selector_service.get_selected_model(
                AvailableProcesses.CLASSIFIER
            )

            self.qualifier_service = OpencodeQualifierService(qualifier_model)
            self.classification_service = OpenCodeClassificationService(
                classifier_model
            )
            start_time = time.perf_counter()
            evaluation_results: list[QualifierResult] = await self.qualify_assessment(
                assessment
            )
            end_time = time.perf_counter()
            evaluation_duration = end_time - start_time
            print(
                f"Evaluation of assessment {assessment.assessment_id} took {evaluation_duration:.6f} seconds."
            )
            await self.save_assessment_results(evaluation_results)
            topic_results: list[TopicResult] = self.get_knowledge_profile(
                assessment.user_id, evaluation_results
            )
            await self.save_knowledge_profile(topic_results)
            qualifications = self.get_answer_qualifications(
                assessment, evaluation_results
            )
            if not qualifications or len(qualifications) == 0:
                logger.warning(
                    "No qualifications generated for assessment %s, skipping classification.",
                    assessment.assessment_id,
                )
                return []
            classification = await self.classify_assessment(qualifications)
            await self.save_classification_result(classification)
            return qualifications

    async def qualify_assessment(self, assessment: Assessment) -> list[QualifierResult]:
        """Send the assessment answers to the qualifier service for evaluation.

        Uses batch qualification with chunking. Falls back to per-item qualify
        if a batch call fails.

        Args:
            assessment (Assessment): The assessment containing the answers to be evaluated.

        Returns:
            list[QualifierResult]: A list of results from the qualifier service.
        """
        if not self.question_repository or not self.qualifier_service:
            raise RuntimeError(
                "Question repository and qualifier service must be initialized before calling qualify_assessment."
            )

        evaluation_results: list[QualifierResult] = []

        # Pre-fetch all rubrics in a single query
        question_ids = [answer.question_id for answer in assessment.answers]
        if not question_ids:
            return evaluation_results

        rubrics_dict = await self.question_repository.get_question_rubrics_bulk(
            question_ids
        )

        # Build (answer, rubric) pairs, skipping answers without rubrics
        pairs = [
            (answer, rubrics_dict[answer.question_id])
            for answer in assessment.answers
            if answer.question_id in rubrics_dict
        ]

        # Chunk the pairs
        chunks = [
            pairs[i : i + self.chunk_size]
            for i in range(0, len(pairs), self.chunk_size)
        ]

        # Process each chunk
        for chunk in chunks:
            chunk_rubrics = [rubric for _, rubric in chunk]
            chunk_answers = [answer for answer, _ in chunk]

            try:
                batch_prompt = BatchQualifierPrompt(
                    rubrics=chunk_rubrics,
                    answers=chunk_answers,
                    qualifier_mode=EnvironmentVariablesConstants.EVALUATION_MODE,
                    user_id=assessment.user_id,
                    assessment_id=assessment.assessment_id,
                )
                batch_results = await self.qualifier_service.qualify_batch(batch_prompt)
                evaluation_results.extend(batch_results)
            except (BatchQualificationError, ValueError):
                logger.warning(
                    "Batch qualification failed for chunk of %d answers, "
                    "falling back to per-item qualify",
                    len(chunk_answers),
                )
                for answer, rubric in chunk:
                    evaluation_results.append(
                        await self.qualifier_service.qualify(
                            QualifierPrompt(
                                rubric=rubric,
                                qualifier_mode=EnvironmentVariablesConstants.EVALUATION_MODE,
                                user_id=assessment.user_id,
                                user_answer=answer.answer,
                                assessment_id=assessment.assessment_id,
                                answer_id=answer.answer_id,
                            )
                        )
                    )

        return evaluation_results

    async def save_assessment_results(self, results: list[QualifierResult]):
        """Save the results of the assessment evaluation to the assessment repository.

        Args:
            results (list[QualifierResult]): A list of results from the qualifier service.
        """
        if not self.assessment_repository:
            raise RuntimeError(
                "Assessment repository must be initialized before calling save_assessment_results."
            )
        for result in results:
            await self.assessment_repository.save_assessment_qualification(result)

    def get_knowledge_profile(
        self, user_id: str, results: list[QualifierResult]
    ) -> list[TopicResult]:
        """Generate a knowledge profile for the user based on the results.

        Args:
            user_id (str): The ID of the user.
            results (list[QualifierResult]): Results from the qualifier service.

        Returns:
            list[TopicResult]: Topic results with averaged scores.
        """
        topic_scores: defaultdict[str, list[int]] = defaultdict(list)
        for result in results:
            topic_scores[result.question_topic].append(result.score)

        topic_results: list[TopicResult] = [
            TopicResult(
                user_id=user_id,
                topic=topic,
                score=round(sum(scores) / len(scores)),
            )
            for topic, scores in topic_scores.items()
        ]
        return topic_results

    async def save_knowledge_profile(self, topic_results: list[TopicResult]):
        """Save the knowledge profile for the user.

        Args:
            topic_results (list[TopicResult]): Topic results to save.
        """
        if not self.assessment_repository:
            raise RuntimeError(
                "Assessment repository must be initialized before calling save_knowledge_profile."
            )
        for topic_result in topic_results:
            await self.assessment_repository.save_topic_result(topic_result)

    def get_answer_qualifications(
        self, assessment: Assessment, evaluation_results: list[QualifierResult]
    ) -> list[QuestionAnswerQualification]:
        """Combine assessment answers with their corresponding evaluation results.

        Args:
            assessment (Assessment): The assessment containing the answers.
            evaluation_results (list[QualifierResult]): Results from the qualifier service.

        Returns:
            list[QuestionAnswerQualification]: A list of question answer qualifications.
        """
        # Create a mapping from answer_id to QualifierResult for quick lookup
        result_map = {result.answer_id: result for result in evaluation_results}

        qualifications: list[QuestionAnswerQualification] = []
        for answer in assessment.answers:
            if answer.answer_id in result_map:
                result = result_map[answer.answer_id]
                qualifications.append(
                    QuestionAnswerQualification(
                        question_id=answer.question_id,
                        user_id=assessment.user_id,
                        assessment_id=assessment.assessment_id,
                        question_difficulty=result.question_difficulty,
                        answer=answer.answer,
                        score=result.score,
                        feedback=result.feedback,
                        key_concepts_detected=result.key_concepts_detected,
                        misconceptions_detected=result.misconceptions_detected,
                    )
                )
            else:
                logger.warning(
                    "No evaluation result found for answer_id: %s", answer.answer_id
                )

        return qualifications

    async def classify_assessment(
        self, answers: list[QuestionAnswerQualification]
    ) -> ClassificationResult:
        """Classify the user's knowledge based on their answers to the assessment questions.

        Args:
            answers (list[QuestionAnswerQualification]): A list of question answer qualifications.

        Returns:
            ClassificationResult: The result of the classification, including classification and feedback.
        """
        if not self.classification_service:
            raise RuntimeError(
                "Classification service must be initialized before calling classify_assessment."
            )
        classification_prompt = ClassificationPrompt(qualifications=answers)
        classification_result = await self.classification_service.classify(
            classification_prompt
        )
        return classification_result

    async def save_classification_result(
        self, classification_result: ClassificationResult
    ):
        """Save the classification result for the user.

        Args:
            classification_result (ClassificationResult): The result of the classification to save.
        """
        if not self.assessment_repository:
            raise RuntimeError(
                "Assessment repository must be initialized before calling save_classification_result."
            )
        await self.assessment_repository.save_classification_result(
            classification_result
        )
