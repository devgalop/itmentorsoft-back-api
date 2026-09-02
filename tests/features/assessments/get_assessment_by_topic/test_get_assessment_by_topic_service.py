from unittest.mock import AsyncMock, patch

import pytest

from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_request import (
    GetAssessmentByTopicRequest,
)
from src.features.assessments.get_assessment_by_topic.get_assessment_by_topic_response import (
    EvaluativeQuestionDataByTopic,
)
from src.features.assessments.shared.get_assessment_service import (
    GetAssessmentService,
    GetRandomQuestionsByTopicRequest,
)
from itmentorsoft_persistence.dto import AssessmentQuiz
from itmentorsoft_persistence.dto import (
    EvaluativeQuestion,
    QuestionDifficulty,
)

VALID_REQUEST = GetAssessmentByTopicRequest(
    topic_id="topic-a1b2c3d4e5f6a7b8c9d0e1f2",
    student_id="a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6",
)

STUDENT_ID = "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
TOPIC_ID = "topic-a1b2c3d4e5f6a7b8c9d0e1f2"
NUMBER_OF_QUESTIONS = (
    5  # This should match the NUMBER_OF_QUESTIONS in the service for testing purposes
)


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
# Tests for generate_assessment_by_topic()
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_when_valid_request_with_enough_questions_per_level_then_should_return_correct_count_and_save_assessment():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.EASY, 5)
    question_repo.get_questions_by_topic = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        _ = await service.generate_assessment_by_topic(VALID_REQUEST)

    assessment_repo.save_assessment.assert_called_once()


@pytest.mark.asyncio
async def test_when_generate_assessment_by_topic_then_should_return_evaluative_question_data_by_topic_objects():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.EASY, 5)
    question_repo.get_questions_by_topic = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        result = await service.generate_assessment_by_topic(VALID_REQUEST)

    for item in result.questions:
        assert isinstance(item, EvaluativeQuestionDataByTopic)
        assert item.question_id is not None
        assert item.text_to_evaluate is not None
        assert item.topic is not None


@pytest.mark.asyncio
async def test_when_generate_assessment_by_topic_then_should_save_assessment_with_correct_student_id():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.EASY, 5)
    question_repo.get_questions_by_topic = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        await service.generate_assessment_by_topic(VALID_REQUEST)

    assessment_repo.save_assessment.assert_called_once()
    saved_quiz: AssessmentQuiz = assessment_repo.save_assessment.call_args[0][0]
    assert isinstance(saved_quiz, AssessmentQuiz)
    assert saved_quiz.user_id == STUDENT_ID


@pytest.mark.asyncio
async def test_when_generate_assessment_by_topic_then_should_query_all_difficulty_levels():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.EASY, 5)
    question_repo.get_questions_by_topic = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        await service.generate_assessment_by_topic(VALID_REQUEST)

    assert question_repo.get_questions_by_topic.call_count == len(QuestionDifficulty)
    question_repo.get_questions_by_topic.assert_any_call(
        topic=TOPIC_ID, difficulty=QuestionDifficulty.EASY
    )
    question_repo.get_questions_by_topic.assert_any_call(
        topic=TOPIC_ID, difficulty=QuestionDifficulty.MEDIUM
    )
    question_repo.get_questions_by_topic.assert_any_call(
        topic=TOPIC_ID, difficulty=QuestionDifficulty.HARD
    )


@pytest.mark.asyncio
async def test_when_not_enough_questions_available_then_should_return_available_count():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    question_repo.get_questions_by_topic = AsyncMock(return_value=[])

    service = GetAssessmentService(question_repo, assessment_repo)

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k]) if k > 0 else []

        result = await service.generate_assessment_by_topic(VALID_REQUEST)

    assert len(result.questions) == 0
    assessment_repo.save_assessment.assert_called_once()


@pytest.mark.asyncio
async def test_when_generate_assessment_by_topic_then_saved_assessment_should_contain_correct_question_ids():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.EASY, 5)
    question_repo.get_questions_by_topic = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        result = await service.generate_assessment_by_topic(VALID_REQUEST)

    saved_quiz: AssessmentQuiz = assessment_repo.save_assessment.call_args[0][0]
    returned_ids = [q.question_id for q in result.questions]
    assert saved_quiz.questions == returned_ids


# ---------------------------------------------------------------------------
# Tests for get_random_questions_by_topic()
# ---------------------------------------------------------------------------


@pytest.mark.asyncio
async def test_when_request_n_questions_by_topic_then_should_return_n_questions():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.MEDIUM, 10)
    question_repo.get_questions_by_topic = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    request = GetRandomQuestionsByTopicRequest(
        number_of_questions=4,
        difficulty_level=QuestionDifficulty.MEDIUM,
        topic_id=TOPIC_ID,
    )

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        result = await service.get_random_questions_by_topic(request)

    assert len(result) == 4


@pytest.mark.asyncio
async def test_when_requests_more_than_available_by_topic_then_should_adjust_to_available_count():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.HARD, 3)
    question_repo.get_questions_by_topic = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    request = GetRandomQuestionsByTopicRequest(
        number_of_questions=10,
        difficulty_level=QuestionDifficulty.HARD,
        topic_id=TOPIC_ID,
    )

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k]) if k > 0 else []

        result = await service.get_random_questions_by_topic(request)

    assert len(result) == 3


@pytest.mark.asyncio
async def test_when_get_random_questions_by_topic_then_should_map_evaluative_question_to_data():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = [
        make_evaluative_question("q-abc", "What is a class?", topic=TOPIC_ID),
        make_evaluative_question("q-def", "What is an object?", topic=TOPIC_ID),
    ]
    question_repo.get_questions_by_topic = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    request = GetRandomQuestionsByTopicRequest(
        number_of_questions=2,
        difficulty_level=QuestionDifficulty.EASY,
        topic_id=TOPIC_ID,
    )

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        result = await service.get_random_questions_by_topic(request)

    assert len(result) == 2
    assert isinstance(result[0], EvaluativeQuestionDataByTopic)
    assert result[0].question_id == "q-abc"
    assert result[0].text_to_evaluate == "What is a class?"
    assert result[0].topic == TOPIC_ID
    assert result[1].question_id == "q-def"
    assert result[1].text_to_evaluate == "What is an object?"
    assert result[1].topic == TOPIC_ID


@pytest.mark.asyncio
async def test_when_get_random_questions_by_topic_then_repository_called_with_correct_topic_and_difficulty():
    question_repo = AsyncMock()
    assessment_repo = AsyncMock()

    pool = make_question_pool(QuestionDifficulty.HARD, 5)
    question_repo.get_questions_by_topic = AsyncMock(return_value=pool)

    service = GetAssessmentService(question_repo, assessment_repo)

    request = GetRandomQuestionsByTopicRequest(
        number_of_questions=2,
        difficulty_level=QuestionDifficulty.HARD,
        topic_id=TOPIC_ID,
    )

    with patch(
        "src.features.assessments.shared.get_assessment_service._rng"
    ) as mock_rng:
        mock_rng.sample.side_effect = lambda seq, k: list(seq[:k])

        await service.get_random_questions_by_topic(request)

    question_repo.get_questions_by_topic.assert_called_once_with(
        topic=TOPIC_ID, difficulty=QuestionDifficulty.HARD
    )
