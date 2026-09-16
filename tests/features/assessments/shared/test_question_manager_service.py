from unittest.mock import AsyncMock, MagicMock
import pytest

from src.features.assessments.register_question.register_question_request import (
    RegisterQuestionRequest,
)
from src.features.assessments.shared.question_manager_service import (
    CreateQuestionRequest,
    QuestionManagerService,
)

VALID_REGISTER_REQUEST = dict(
    text="Explain the difference between abstraction and encapsulation in OOP",
    concept="Object Oriented Programming",
    definition="OOP is a programming paradigm based on objects and classes",
    simple_explanation="OOP groups data and behavior together into reusable objects",
    correct_sample="Abstraction hides implementation details while encapsulation bundles data",
    wrong_sample="They are the same thing, both hide data from the user completely",
    common_misconception=[
        "Abstraction and encapsulation are the same concept in OOP",
        "Encapsulation only refers to using private fields inside a class",
    ],
    rubric=[{"score": 3, "criteria": "Complete and correct answer with examples"}],
    semantic_keywords=["OOP", "abstraction"],
    difficulty="intermedio",
    topic="Object Oriented Programming",
)


def _make_mock_builder_instance(question_id: str = "q-123"):
    """Create a mock QuestionBuilder instance with chainable methods and a .build() result."""
    mock_question = MagicMock()
    mock_question.question_id = question_id

    mock_builder = MagicMock()
    # All setter methods return self for chaining
    mock_builder.set_text_to_evaluate.return_value = mock_builder
    mock_builder.set_concept.return_value = mock_builder
    mock_builder.set_definition.return_value = mock_builder
    mock_builder.set_simple_explanation.return_value = mock_builder
    mock_builder.set_correct_sample.return_value = mock_builder
    mock_builder.set_wrong_sample.return_value = mock_builder
    mock_builder.add_common_misconceptions.return_value = mock_builder
    mock_builder.add_semantic_keywords.return_value = mock_builder
    mock_builder.add_rubrics.return_value = mock_builder
    mock_builder.set_version.return_value = mock_builder
    mock_builder.set_classification.return_value = mock_builder
    mock_builder.set_difficulty.return_value = mock_builder
    mock_builder.build.return_value = mock_question

    return mock_builder, mock_question


def _make_admin_user(email: str):
    """Create a simple mock object with email and username attributes."""
    user = MagicMock()
    user.email = email
    user.username = email.split("@")[0]
    return user


@pytest.mark.asyncio
async def test_create_question_happy_path_with_admin_users():
    """Question is saved, notifications sent to each admin, returns success with question_id."""
    # Arrange
    question_repository = AsyncMock()
    question_repository.save_question = AsyncMock()

    mock_builder, mock_question = _make_mock_builder_instance("q-123")
    question_builder_cls = MagicMock(return_value=mock_builder)

    notification_service = AsyncMock()
    notification_service.send_notification = AsyncMock(return_value=True)

    template_loader = MagicMock()
    template_loader.load.return_value = "Hello %REVIEWER%, %CREATED_BY% created %OBJECT_NAME% (%OBJECT_CODE%) on %CREATED_DATE%. Review at %URL_REVIEW%."

    user_repository = AsyncMock()
    admin1 = _make_admin_user("admin1@example.com")
    admin2 = _make_admin_user("admin2@example.com")
    user_repository.get_admin_users = AsyncMock(return_value=[admin1, admin2])

    service = QuestionManagerService(
        question_repository=question_repository,
        question_builder=question_builder_cls,
        notification_service=notification_service,
        template_loader=template_loader,
        user_repository=user_repository,
    )

    request_model = RegisterQuestionRequest(**VALID_REGISTER_REQUEST)
    request = CreateQuestionRequest(model=request_model, user_name="john_doe")

    # Act
    response = await service.create_question(request)

    # Assert
    assert response.is_success is True
    assert response.question_id == "q-123"
    assert response.message == "Question created successfully"

    question_repository.save_question.assert_called_once()
    user_repository.get_admin_users.assert_called_once()
    template_loader.load.assert_called_once_with("item_created")

    # Two notifications sent (one per admin)
    assert notification_service.send_notification.call_count == 2


@pytest.mark.asyncio
async def test_create_question_happy_path_without_admin_users():
    """Question saved, no notifications sent, returns success."""
    # Arrange
    question_repository = AsyncMock()
    question_repository.save_question = AsyncMock()

    mock_builder, mock_question = _make_mock_builder_instance("q-456")
    question_builder_cls = MagicMock(return_value=mock_builder)

    notification_service = AsyncMock()
    notification_service.send_notification = AsyncMock(return_value=True)

    template_loader = MagicMock()

    user_repository = AsyncMock()
    user_repository.get_admin_users = AsyncMock(return_value=[])

    service = QuestionManagerService(
        question_repository=question_repository,
        question_builder=question_builder_cls,
        notification_service=notification_service,
        template_loader=template_loader,
        user_repository=user_repository,
    )

    request_model = RegisterQuestionRequest(**VALID_REGISTER_REQUEST)
    request = CreateQuestionRequest(model=request_model, user_name="jane_doe")

    # Act
    response = await service.create_question(request)

    # Assert
    assert response.is_success is True
    assert response.question_id == "q-456"
    assert response.message == "Question created successfully"

    question_repository.save_question.assert_called_once()
    user_repository.get_admin_users.assert_called_once()
    # No notifications sent
    notification_service.send_notification.assert_not_called()
    # Template not loaded since no admins
    template_loader.load.assert_not_called()


@pytest.mark.asyncio
async def test_create_question_exception_during_save():
    """Returns is_success=False with error message when save raises."""
    # Arrange
    question_repository = AsyncMock()
    question_repository.save_question = AsyncMock(
        side_effect=Exception("Database connection failed")
    )

    mock_builder, mock_question = _make_mock_builder_instance("q-789")
    question_builder_cls = MagicMock(return_value=mock_builder)

    notification_service = AsyncMock()
    template_loader = MagicMock()
    user_repository = AsyncMock()

    service = QuestionManagerService(
        question_repository=question_repository,
        question_builder=question_builder_cls,
        notification_service=notification_service,
        template_loader=template_loader,
        user_repository=user_repository,
    )

    request_model = RegisterQuestionRequest(**VALID_REGISTER_REQUEST)
    request = CreateQuestionRequest(model=request_model, user_name="test_user")

    # Act
    response = await service.create_question(request)

    # Assert
    assert response.is_success is False
    assert "Error creating question" in response.message
    assert response.question_id == ""


@pytest.mark.asyncio
async def test_create_question_exception_during_notification():
    """Returns is_success=False when notification sending raises (whole method wrapped in try/except)."""
    # Arrange
    question_repository = AsyncMock()
    question_repository.save_question = AsyncMock()

    mock_builder, mock_question = _make_mock_builder_instance("q-notify-fail")
    question_builder_cls = MagicMock(return_value=mock_builder)

    notification_service = AsyncMock()
    # First call succeeds, second call fails
    notification_service.send_notification = AsyncMock(
        side_effect=[True, Exception("SMTP server unreachable")]
    )

    template_loader = MagicMock()
    template_loader.load.return_value = "Hello %REVIEWER%, %CREATED_BY% created %OBJECT_NAME% (%OBJECT_CODE%) on %CREATED_DATE%. Review at %URL_REVIEW%."

    user_repository = AsyncMock()
    admin1 = _make_admin_user("admin1@example.com")
    admin2 = _make_admin_user("admin2@example.com")
    user_repository.get_admin_users = AsyncMock(return_value=[admin1, admin2])

    service = QuestionManagerService(
        question_repository=question_repository,
        question_builder=question_builder_cls,
        notification_service=notification_service,
        template_loader=template_loader,
        user_repository=user_repository,
    )

    request_model = RegisterQuestionRequest(**VALID_REGISTER_REQUEST)
    request = CreateQuestionRequest(model=request_model, user_name="test_user")

    # Act
    response = await service.create_question(request)

    # Assert
    assert response.is_success is False
    assert "Error creating question" in response.message
