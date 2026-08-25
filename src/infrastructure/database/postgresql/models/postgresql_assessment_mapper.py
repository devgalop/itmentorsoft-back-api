from datetime import datetime

from src.features.assessments.shared.assessment import (
    Assessment,
    AssessmentAnswer,
    AssessmentQuiz,
    AssessmentSummary,
)
from src.features.assessments.shared.classification_service import ClassificationResult
from src.features.assessments.shared.qualifier_service import (
    QualifierResult,
    TopicResult,
)
from src.features.reports.shared.student_report import (
    StudentAnswerScore,
    StudentAssessmentResult,
    StudentKnowledgeProfile,
)
from src.infrastructure.database.postgresql.models.postgresql_assessment_model import (
    AssessmentAnswerEntity,
    AssessmentEntity,
    AssessmentMisconceptionEntity,
    AssessmentQualificationEntity,
    AssessmentQualificationKeyConceptEntity,
    AssessmentQuizEntity,
    ClassificationResultEntity,
    TopicResultEntity,
)


class PostgresAssessmentMapper:
    @staticmethod
    def to_entity(request: Assessment) -> AssessmentEntity:
        answers = [
            PostgresAssessmentAnswerMapper.to_entity(ans) for ans in request.answers
        ]
        return AssessmentEntity(
            id=request.assessment_id,
            user_id=request.user_id,
            created_at=request.created_at,
            answers=answers,
        )

    @staticmethod
    def to_model(entity: AssessmentEntity) -> Assessment:
        answers = [
            PostgresAssessmentAnswerMapper.to_model(ans) for ans in entity.answers
        ]
        assessment = Assessment(
            assessment_id=entity.id,
            user_id=entity.user_id,
            created_at=entity.created_at,
            answers=answers,
        )
        return assessment

    @staticmethod
    def to_assessment_result(entity: AssessmentEntity) -> StudentAssessmentResult:
        answer_scores = []
        for qualification in entity.qualifications:
            answer_score = StudentAnswerScore(
                question_id=qualification.question_id,
                question_text=next(
                    (
                        q.question.text
                        for q in entity.answers
                        if q.question_id == qualification.question_id
                    ),
                    "",
                ),
                answer=next(
                    (
                        ans.answer
                        for ans in entity.answers
                        if ans.id == qualification.answer_id
                    ),
                    "",
                ),
                score=qualification.score,
                feedback=qualification.feedback,
                misconceptions=[
                    mc.misconception for mc in qualification.misconceptions
                ],
                key_concepts=[kc.key_concept for kc in qualification.key_concepts],
            )
            answer_scores.append(answer_score)

        avg_score = (
            sum(qualification.score for qualification in entity.qualifications)
            / len(entity.qualifications)
            if entity.qualifications
            else 0.0
        )

        return StudentAssessmentResult(
            assessment_id=entity.id,
            student_id=entity.user_id,
            avg_score=avg_score,
            classification=(
                entity.classification_result.classification
                if entity.classification_result
                else ""
            ),
            feedback=(
                entity.classification_result.feedback
                if entity.classification_result
                else ""
            ),
            answer_scores=answer_scores,
        )

    @staticmethod
    def quiz_question_entity(
        request: AssessmentQuiz, question_id: str
    ) -> AssessmentQuizEntity:
        return AssessmentQuizEntity(
            assessment_id=request.assessment_id,
            question_id=question_id,
            created_at=request.created_at,
        )

    @staticmethod
    def quiz_to_assessment_entity(quiz: AssessmentQuiz) -> AssessmentEntity:
        return AssessmentEntity(
            id=quiz.assessment_id,
            user_id=quiz.user_id,
            created_at=quiz.created_at,
        )

    @staticmethod
    def quiz_to_model(entity: AssessmentEntity) -> AssessmentQuiz:
        questions_ids = [q.question_id for q in entity.questions]
        assessment_quiz = AssessmentQuiz(
            assessment_id=entity.id,
            user_id=entity.user_id,
            created_at=entity.created_at,
            questions=questions_ids,
        )
        return assessment_quiz

    @staticmethod
    def answer_to_entity(answer: AssessmentAnswer) -> AssessmentAnswerEntity:
        return PostgresAssessmentAnswerMapper.to_entity(answer)

    @staticmethod
    def qualifier_result_to_entity(
        qualifier_result: QualifierResult,
    ) -> AssessmentQualificationEntity:
        return PostgresAssessmentQualificationMapper.to_entity(qualifier_result)

    @staticmethod
    def qualifier_result_key_concept_to_entity(
        qualification_id: str, key_concept: str
    ) -> AssessmentQualificationKeyConceptEntity:
        return PostgresAssessmentQualificationMapper.to_key_concepts_entity(
            qualification_id, key_concept
        )

    @staticmethod
    def qualifier_result_misconception_to_entity(
        qualification_id: str, misconception: str
    ) -> AssessmentMisconceptionEntity:
        return PostgresAssessmentQualificationMapper.to_misconceptions_entity(
            qualification_id, misconception
        )

    @staticmethod
    def topic_result_to_entity(topic_result: TopicResult) -> TopicResultEntity:
        return PostgresTopicResultMapper.to_entity(topic_result)

    @staticmethod
    def topic_result_to_model(entity: TopicResultEntity) -> TopicResult:
        return PostgresTopicResultMapper.to_model(entity)

    @staticmethod
    def topic_result_to_knowledge_profile(
        entity: TopicResultEntity,
    ) -> StudentKnowledgeProfile:
        return PostgresTopicResultMapper.to_knowledge_profile(entity)

    @staticmethod
    def classification_result_to_entity(
        classification_result: ClassificationResult,
    ) -> ClassificationResultEntity:
        return PostgresClassificationResultMapper.to_entity(classification_result)

    @staticmethod
    def assessment_entity_to_summary(entity: AssessmentEntity) -> AssessmentSummary:
        avg_score = (
            sum(qualification.score for qualification in entity.qualifications)
            / len(entity.qualifications)
            if entity.qualifications
            else 0.0
        )
        return AssessmentSummary(
            assessment_id=entity.id,
            score=avg_score,
            date_taken=entity.created_at.strftime("%Y-%m-%d %H:%M"),
            classification=(
                entity.classification_result.classification
                if entity.classification_result
                else None
            ),
            feedback=(
                entity.classification_result.feedback
                if entity.classification_result
                else None
            ),
        )


class PostgresAssessmentAnswerMapper:
    @staticmethod
    def to_entity(request: AssessmentAnswer) -> AssessmentAnswerEntity:
        return AssessmentAnswerEntity(
            id=request.answer_id,
            assessment_id=request.assessment_id,
            question_id=request.question_id,
            answer=request.answer,
            time_taken_seconds=request.time_taken_seconds,
        )

    @staticmethod
    def to_model(entity: AssessmentAnswerEntity) -> AssessmentAnswer:
        return AssessmentAnswer(
            answer_id=entity.id,
            assessment_id=entity.assessment_id,
            question_id=entity.question_id,
            answer=entity.answer,
            time_taken_seconds=entity.time_taken_seconds,
        )


class PostgresAssessmentQualificationMapper:
    @staticmethod
    def to_entity(model: QualifierResult) -> AssessmentQualificationEntity:
        return AssessmentQualificationEntity(
            id=model.id,
            assessment_id=model.assessment_id,
            question_id=model.question_id,
            user_id=model.user_id,
            answer_id=model.answer_id,
            score=model.score,
            feedback=model.feedback,
            question_topic=model.question_topic,
            question_difficulty=model.question_difficulty,
        )

    @staticmethod
    def to_key_concepts_entity(
        qualification_id: str, key_concept: str
    ) -> AssessmentQualificationKeyConceptEntity:
        return AssessmentQualificationKeyConceptEntity(
            qualification_id=qualification_id, key_concept=key_concept
        )

    @staticmethod
    def to_misconceptions_entity(
        qualification_id: str, misconception: str
    ) -> AssessmentMisconceptionEntity:
        return AssessmentMisconceptionEntity(
            qualification_id=qualification_id, misconception=misconception
        )

    @staticmethod
    def to_model(entity: AssessmentQualificationEntity) -> QualifierResult:
        key_concepts = [kc.key_concept for kc in entity.key_concepts]
        misconceptions = [mc.misconception for mc in entity.misconceptions]
        return QualifierResult(
            id=entity.id,
            question_id=entity.question_id,
            user_id=entity.user_id,
            score=entity.score,
            feedback=entity.feedback,
            key_concepts_detected=key_concepts,
            misconceptions_detected=misconceptions,
            question_topic=entity.question_topic,
            assessment_id=entity.assessment_id,
            question_difficulty=entity.question_difficulty,
            answer_id=entity.answer_id,
        )


class PostgresTopicResultMapper:
    @staticmethod
    def to_entity(topic_result: TopicResult) -> TopicResultEntity:
        date_now = datetime.now()
        return TopicResultEntity(
            user_id=topic_result.user_id,
            topic=topic_result.topic,
            score=topic_result.score,
            created_at=date_now,
            updated_at=date_now,
            is_enabled=True,
        )

    @staticmethod
    def to_model(entity: TopicResultEntity) -> TopicResult:
        return TopicResult(
            user_id=entity.user_id,
            topic=entity.topic,
            score=entity.score,
        )

    @staticmethod
    def to_knowledge_profile(entity: TopicResultEntity) -> StudentKnowledgeProfile:
        return StudentKnowledgeProfile(
            topic=entity.topic,
            score=entity.score,
        )


class PostgresClassificationResultMapper:
    @staticmethod
    def to_entity(
        classification_result: ClassificationResult,
    ) -> ClassificationResultEntity:
        return ClassificationResultEntity(
            user_id=classification_result.user_id,
            assessment_id=classification_result.assessment_id,
            classification=classification_result.classification,
            feedback=classification_result.feedback,
            is_enabled=True,
        )
