import json
from unittest.mock import MagicMock, patch

import pytest

from src.features.assessments.shared.assessment import AssessmentAnswer
from src.features.assessments.shared.qualifier_service import (
    BatchQualificationError,
    BatchQualifierPrompt,
)
from src.features.assessments.shared.question import QuestionBuilder
from src.infrastructure.qualifier.opencode_qualifier_service import (
    OpencodeQualifierService,
)


def _make_rubric(question_id: str) -> QuestionBuilder:
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


def _make_batch_prompt(
    count: int = 2,
) -> tuple[BatchQualifierPrompt, list, list]:
    """Create a batch prompt with `count` rubrics and answers."""
    rubrics = [_make_rubric(f"q-{i:03d}") for i in range(1, count + 1)]
    answers = [_make_answer(f"a-{i:03d}", f"q-{i:03d}") for i in range(1, count + 1)]
    prompt = BatchQualifierPrompt(
        rubrics=rubrics,
        answers=answers,
        qualifier_mode="normal",
        user_id="user-001",
        assessment_id="assess-001",
    )
    return prompt, rubrics, answers


def _make_json_result(answer_id: str, score: int = 80) -> dict:
    return {
        "answer_id": answer_id,
        "score": score,
        "feedback": "Good answer",
        "key_concepts_detected": ["concept1"],
        "misconceptions_detected": [],
    }


class TestOpencodeBatchQualification:
    """Tests for OpencodeQualifierService.qualify_batch."""

    @pytest.fixture
    def service(self):
        """Create a service with a mocked OpenAI client."""
        with patch(
            "src.infrastructure.qualifier.opencode_qualifier_service.OpenAI"
        ) as mock_openai:
            mock_client = MagicMock()
            mock_openai.return_value = mock_client
            svc = OpencodeQualifierService(model_id="test-model")
            svc.client = mock_client
            return svc

    @pytest.mark.asyncio
    async def test_valid_json_array_returns_results_in_input_order(self, service):
        """GIVEN a batch of 3 answers with valid JSON array response
        WHEN qualify_batch is called
        THEN results are returned in the same order as input answers.
        """
        prompt, rubrics, answers = _make_batch_prompt(3)

        # LLM returns results in shuffled order
        llm_response = json.dumps(
            [
                _make_json_result("a-003", 90),
                _make_json_result("a-001", 80),
                _make_json_result("a-002", 85),
            ]
        )

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = llm_response
        service.client.chat.completions.create.return_value = mock_completion

        results = await service.qualify_batch(prompt)

        assert len(results) == 3
        # Results should be in input order: a-001, a-002, a-003
        assert results[0].answer_id == "a-001"
        assert results[0].score == 80
        assert results[1].answer_id == "a-002"
        assert results[1].score == 85
        assert results[2].answer_id == "a-003"
        assert results[2].score == 90

    @pytest.mark.asyncio
    async def test_orphan_result_discarded_with_warning(self, service):
        """GIVEN LLM returns a result with answer_id not in the batch
        WHEN qualify_batch is called
        THEN that result is discarded.
        """
        prompt, rubrics, answers = _make_batch_prompt(2)

        llm_response = json.dumps(
            [
                _make_json_result("a-001", 80),
                _make_json_result("a-999", 70),  # orphan
                _make_json_result("a-002", 85),
            ]
        )

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = llm_response
        service.client.chat.completions.create.return_value = mock_completion

        with patch(
            "src.infrastructure.qualifier.opencode_qualifier_service.logger"
        ) as mock_logger:
            results = await service.qualify_batch(prompt)

        assert len(results) == 2
        result_ids = [r.answer_id for r in results]
        assert "a-999" not in result_ids
        mock_logger.warning.assert_called_once()

    @pytest.mark.asyncio
    async def test_malformed_json_raises_batch_qualification_error(self, service):
        """GIVEN LLM returns a response that is not valid JSON
        WHEN qualify_batch is called
        THEN BatchQualificationError is raised with raw_response attached.
        """
        prompt, rubrics, answers = _make_batch_prompt(2)

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "this is not json at all"
        service.client.chat.completions.create.return_value = mock_completion

        with pytest.raises(BatchQualificationError) as exc_info:
            await service.qualify_batch(prompt)

        assert exc_info.value.raw_response == "this is not json at all"

    @pytest.mark.asyncio
    async def test_json_object_not_array_raises_batch_qualification_error(
        self, service
    ):
        """GIVEN LLM returns a JSON object instead of an array
        WHEN qualify_batch is called
        THEN BatchQualificationError is raised.
        """
        prompt, rubrics, answers = _make_batch_prompt(2)

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = json.dumps(
            {
                "answer_id": "a-001",
                "score": 80,
                "feedback": "ok",
                "key_concepts_detected": [],
                "misconceptions_detected": [],
            }
        )
        service.client.chat.completions.create.return_value = mock_completion

        with pytest.raises(BatchQualificationError):
            await service.qualify_batch(prompt)

    @pytest.mark.asyncio
    async def test_empty_response_raises_value_error(self, service):
        """GIVEN LLM returns an empty response
        WHEN qualify_batch is called
        THEN ValueError is raised.
        """
        prompt, rubrics, answers = _make_batch_prompt(2)

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = None
        service.client.chat.completions.create.return_value = mock_completion

        with pytest.raises(ValueError, match="empty response"):
            await service.qualify_batch(prompt)

    @pytest.mark.asyncio
    async def test_llm_called_once_per_batch(self, service):
        """GIVEN a batch prompt with 7 rubrics
        WHEN qualify_batch is called
        THEN exactly one OpenAI API call is made.
        """
        prompt, rubrics, answers = _make_batch_prompt(7)

        llm_response = json.dumps(
            [_make_json_result(f"a-{i:03d}", 80) for i in range(1, 8)]
        )

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = llm_response
        service.client.chat.completions.create.return_value = mock_completion

        await service.qualify_batch(prompt)

        service.client.chat.completions.create.assert_called_once()

    @pytest.mark.asyncio
    async def test_result_fields_populated_correctly(self, service):
        """GIVEN valid batch response
        WHEN qualify_batch is called
        THEN each QualifierResult has all fields populated correctly.
        """
        prompt, rubrics, answers = _make_batch_prompt(1)

        llm_response = json.dumps(
            [
                {
                    "answer_id": "a-001",
                    "score": 75,
                    "feedback": "Decent answer",
                    "key_concepts_detected": ["oop", "inheritance"],
                    "misconceptions_detected": ["confuses class with instance"],
                }
            ]
        )

        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = llm_response
        service.client.chat.completions.create.return_value = mock_completion

        results = await service.qualify_batch(prompt)

        assert len(results) == 1
        r = results[0]
        assert r.answer_id == "a-001"
        assert r.score == 75
        assert r.feedback == "Decent answer"
        assert r.key_concepts_detected == ["oop", "inheritance"]
        assert r.misconceptions_detected == ["confuses class with instance"]
        assert r.user_id == "user-001"
        assert r.assessment_id == "assess-001"
        assert r.question_id == "q-001"
