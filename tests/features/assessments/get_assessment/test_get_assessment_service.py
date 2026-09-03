from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.features.assessments.get_assessment.get_assessment_request import (
    GetAssessmentRequest,
)
from src.features.assessments.get_assessment.get_assessment_response import (
    EvaluativeQuestionData,
)
from src.features.assessments.shared.get_assessment_service import (
    GetAssessmentService,
    GetRandomQuestionsRequest,
)
from itmentorsoft_persistence.dto import AssessmentQuiz
from itmentorsoft_persistence.dto import (
    EvaluativeQuestion,
    QuestionDifficulty,
)

VALID_REQUEST = GetAssessmentRequest(student_id="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6")
NUMBER_OF_QUESTIONS = (
    6  # This should match the NUMBER_OF_QUESTIONS in the service for testing purposes
)
STUDENT_ID = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"


def make_evaluative_question(
    question_id: str, text: str, topic: str = "test-topic"
) -> EvaluativeQuestion:
    return EvaluativeQuestion(
        question_id=question_id, text_to_evaluate=text, topic=topic
    )


def make_question_pool(
    difficulty: QuestionDifficulty, count: int
) -> list[EvaluativeQuestion]:
    return [
        make_evaluative_question(
            f"{difficulty.name.lower()}-q{i}", f"Question {i} ({difficulty.name})"
        )
        for i in range(count)
    ]


# ---------------------------------------------------------------------------
# Tests for generate_assessment()
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_when_valid_request_with_enough_questions_per_level_then_should_return_correct_count_and_save_assessment():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.EASY, 5)
    question_repo.get_question_by_level = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        _ = await service.generate_assessment(VALID_REQUEST)

    assessment_repo.save_assessment.assert_called_once()


@pytest.mark.asyncio
async def test_when_generate_assessment_then_should_return_evaluative_question_data_objects():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.EASY, 5)
    question_repo.get_question_by_level = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        result = await service.generate_assessment(VALID_REQUEST)

    for item in result.questions:
        assert isinstance(item, EvaluativeQuestionData)
        assert item.question_id is not None
        assert item.text_to_evaluate is not None


@pytest.mark.asyncio
async def test_when_generate_assessment_then_should_save_assessment_with_correct_student_id():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.EASY, 5)
    question_repo.get_question_by_level = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        await service.generate_assessment(VALID_REQUEST)

    assessment_repo.save_assessment.assert_called_once()
    saved_quiz: AssessmentQuiz = assessment_repo.save_assessment.call_args[0][0]
    assert isinstance(saved_quiz, AssessmentQuiz)
    assert saved_quiz.user_id == STUDENT_ID


@pytest.mark.asyncio
async def test_when_generate_assessment_then_should_query_all_difficulty_levels():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.EASY, 5)
    question_repo.get_question_by_level = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        await service.generate_assessment(VALID_REQUEST)

    assert question_repo.get_question_by_level.call_count == len(QuestionDifficulty)
    question_repo.get_question_by_level.assert_any_call(
        difficulty=QuestionDifficulty.EASY
    )
    question_repo.get_question_by_level.assert_any_call(
        difficulty=QuestionDifficulty.MEDIUM
    )
    question_repo.get_question_by_level.assert_any_call(
        difficulty=QuestionDifficulty.HARD
    )


@pytest.mark.asyncio
async def test_when_not_enough_questions_available_then_should_return_available_count():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    question_repo.get_question_by_level = AsyncMock(return_value=[])

    service = GetAssessmentService(question_repo, assessment_repo)

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k]) if k > 0 else []

        result = await service.generate_assessment(VALID_REQUEST)

    assert len(result.questions) == 0
    assessment_repo.save_assessment.assert_called_once()


@pytest.mark.asyncio
async def test_when_generate_assessment_then_saved_assessment_should_contain_correct_question_ids():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.EASY, 5)
    question_repo.get_question_by_level = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        result = await service.generate_assessment(VALID_REQUEST)

    saved_quiz: AssessmentQuiz = assessment_repo.save_assessment.call_args[0][0]
    returned_ids = [q.question_id for q in result.questions]
    assert saved_quiz.questions == returned_ids


# ---------------------------------------------------------------------------
# Tests for is_initial_assessment()
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_when_no_prior_assessments_then_should_return_true():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()
    assessment_repo.has_first_assessment = AsyncMock(return_value=False)

    service = GetAssessmentService(question_repo, assessment_repo)

    result = await service.is_initial_assessment(STUDENT_ID)

    assert result is True
    assessment_repo.has_first_assessment.assert_called_once_with(STUDENT_ID)


@pytest.mark.asyncio
async def test_when_has_prior_assessments_then_should_return_false():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()
    assessment_repo.has_first_assessment = AsyncMock(return_value=True)

    service = GetAssessmentService(question_repo, assessment_repo)

    result = await service.is_initial_assessment(STUDENT_ID)

    assert result is False
    assessment_repo.has_first_assessment.assert_called_once_with(STUDENT_ID)


# ---------------------------------------------------------------------------
# Tests for get_random_questions()
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_when_request_n_questions_then_should_return_n_questions():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.MEDIUM, 10)
    question_repo.get_question_by_level = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    request = GetRandomQuestionsRequest(
        number_of_questions=4, difficulty_level=QuestionDifficulty.MEDIUM
    )

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        result = await service.get_random_questions(request)

    assert len(result) == 4


@pytest.mark.asyncio
async def test_when_requests_more_than_available_then_should_adjust_to_available_count():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.HARD, 3)
    question_repo.get_question_by_level = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    request = GetRandomQuestionsRequest(
        number_of_questions=10, difficulty_level=QuestionDifficulty.HARD
    )

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k]) if k > 0 else []

        result = await service.get_random_questions(request)

    assert len(result) == 3


@pytest.mark.asyncio
async def test_when_get_random_questions_then_should_map_evaluative_question_to_data():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = [
        make_evaluative_question("q-abc", "What is a class?"),
        make_evaluative_question("q-def", "What is an object?"),
    ]
    question_repo.get_question_by_level = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    request = GetRandomQuestionsRequest(
        number_of_questions=2, difficulty_level=QuestionDifficulty.EASY
    )

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        result = await service.get_random_questions(request)

    assert len(result) == 2
    assert isinstance(result[0], EvaluativeQuestionData)
    assert result[0].question_id == "q-abc"
    assert result[0].text_to_evaluate == "What is a class?"
    assert result[1].question_id == "q-def"
    assert result[1].text_to_evaluate == "What is an object?"


@pytest.mark.asyncio
async def test_when_get_random_questions_then_repository_called_with_correct_difficulty():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.HARD, 5)
    question_repo.get_question_by_level = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    request = GetRandomQuestionsRequest(
        number_of_questions=2, difficulty_level=QuestionDifficulty.HARD
    )

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        await service.get_random_questions(request)

    question_repo.get_question_by_level.assert_called_once_with(
        difficulty=QuestionDifficulty.HARD
    )


# ---------------------------------------------------------------------------
# General tests
# ---------------------------------------------------------------------------


def test_when_service_constructed_then_should_assign_repositories_correctly():
    question_repo = Mock()
    assessment_repo = Mock()

    service = GetAssessmentService(question_repo, assessment_repo)

    assert service.question_repository is question_repo
    assert service.assessment_repository is assessment_repo
