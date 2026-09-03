import pytest

from itmentorsoft_persistence.dto import AssessmentAnswer
from src.features.assessments.shared.qualifier_service import (
    BatchQualificationError,
    BatchQualifierPrompt,
    QualifierService,
)
from itmentorsoft_persistence.dto import Question, QuestionBuilder


def _make_rubric(question_id: str) -> Question:
    return (
        QuestionBuilder()
        .set_question_id(question_id)
        .set_text_to_evaluate(f"Question: {question_id}")
        .set_concept("Test concept")
        .set_definition("Test definition")
        .set_simple_explanation("Test explanation")
        .set_correct_sample("Correct")
        .set_wrong_sample("Wrong")
        .add_rubric(100, "Excellent")
        .add_rubric(50, "Partial")
        .build()
    )


def _make_answer(
    answer_id: str, question_id: str, answer_text: str = "Test answer"
) -> AssessmentAnswer:
    return AssessmentAnswer(
        answer_id=answer_id,
        assessment_id="assess-001",
        question_id=question_id,
        answer=answer_text,
        time_taken_seconds=30,
    )


class TestBatchQualifierPromptConstruction:
    """Tests for BatchQualifierPrompt data class construction."""

    def test_when_constructed_then_all_fields_populated(self):
        """GIVEN rubrics, answers, mode, user_id, assessment_id
        WHEN BatchQualifierPrompt is constructed
        THEN all fields are populated correctly.
        """
        rubrics = [_make_rubric("q-001"), _make_rubric("q-002")]
        answers = [
            _make_answer("a-001", "q-001"),
            _make_answer("a-002", "q-002"),
        ]

        prompt = BatchQualifierPrompt(
            rubrics=rubrics,
            answers=answers,
            qualifier_mode="normal",
            user_id="user-001",
            assessment_id="assess-001",
        )

        assert len(prompt.rubrics) == 2
        assert len(prompt.answers) == 2
        assert prompt.qualifier_mode == "normal"
        assert prompt.user_id == "user-001"
        assert prompt.assessment_id == "assess-001"

    def test_when_empty_lists_then_prompt_still_constructs(self):
        """GIVEN empty rubrics and answers lists
        WHEN BatchQualifierPrompt is constructed
        THEN the prompt constructs with empty collections.
        """
        prompt = BatchQualifierPrompt(
            rubrics=[],
            answers=[],
            qualifier_mode="strict",
            user_id="user-001",
            assessment_id="assess-001",
        )

        assert prompt.rubrics == []
        assert prompt.answers == []
        assert prompt.qualifier_mode == "strict"


class TestBatchQualificationError:
    """Tests for BatchQualificationError exception."""

    def test_when_created_then_raw_response_attached(self):
        """GIVEN a malformed LLM response
        WHEN BatchQualificationError is raised
        THEN the raw_response is accessible on the exception.
        """
        raw = "this is not json"
        err = BatchQualificationError(raw_response=raw)

        assert err.raw_response == raw
        assert "Failed to parse batch qualification response" in str(err)

    def test_when_custom_message_then_message_overrides_default(self):
        """GIVEN a custom error message
        WHEN BatchQualificationError is raised
        THEN the custom message is used.
        """
        err = BatchQualificationError(
            raw_response="{bad", message="Custom parse failure"
        )

        assert err.raw_response == "{bad"
        assert "Custom parse failure" in str(err)


class TestQualifierServiceAbstractContract:
    """Tests that QualifierService declares the qualify_batch abstract method."""

    def test_qualify_batch_is_abstract(self):
        """GIVEN QualifierService base class
        WHEN checking for qualify_batch method
        THEN it is declared as abstract (cannot instantiate directly).
        """
        # QualifierService itself should not be instantiable due to abstract methods
        with pytest.raises(TypeError):
            QualifierService()  # type: ignore

    def test_qualify_batch_exists_on_abstract_class(self):
        """GIVEN QualifierService base class
        WHEN inspecting its methods
        THEN qualify_batch is declared.
        """
        assert hasattr(QualifierService, "qualify_batch")
