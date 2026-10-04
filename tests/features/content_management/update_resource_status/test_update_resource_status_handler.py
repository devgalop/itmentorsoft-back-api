from unittest.mock import AsyncMock
import pytest

from src.features.content_management.update_resource_status.update_resource_status_handler import (
    UpdateResourceStatusHandler,
)
from src.features.content_management.update_resource_status.update_resource_status_request import (
    UpdateResourceStatusRequest,
)


@pytest.mark.asyncio
async def test_when_repository_returns_true_should_return_success():
    content_repository = AsyncMock()
    content_repository.update_resource_status = AsyncMock(return_value=True)

    handler = UpdateResourceStatusHandler(content_repository)
    request = UpdateResourceStatusRequest(content_id="content_123", status=True)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.message == "El estado del contenido ha sido actualizado"
    assert response.content_id == "content_123"
    assert response.new_status is True
    content_repository.update_resource_status.assert_called_once_with(
        content_id="content_123", new_status=True
    )


@pytest.mark.asyncio
async def test_when_repository_returns_false_should_return_failure():
    content_repository = AsyncMock()
    content_repository.update_resource_status = AsyncMock(return_value=False)

    handler = UpdateResourceStatusHandler(content_repository)
    request = UpdateResourceStatusRequest(content_id="content_123", status=False)
    response = await handler.handle(request)

    assert response.is_success is False
    assert response.message == "El estado no puede ser actualizado"
    assert response.content_id == ""
    assert response.new_status is False
    content_repository.update_resource_status.assert_called_once_with(
        content_id="content_123", new_status=False
    )


@pytest.mark.asyncio
async def test_when_repository_raises_exception_should_propagate():
    content_repository = AsyncMock()
    content_repository.update_resource_status = AsyncMock(
        side_effect=Exception("Database connection failed")
    )

    handler = UpdateResourceStatusHandler(content_repository)
    request = UpdateResourceStatusRequest(content_id="content_123", status=True)

    with pytest.raises(Exception, match="Database connection failed"):
        await handler.handle(request)


@pytest.mark.asyncio
async def test_when_updating_to_false_status_should_return_success():
    content_repository = AsyncMock()
    content_repository.update_resource_status = AsyncMock(return_value=True)

    handler = UpdateResourceStatusHandler(content_repository)
    request = UpdateResourceStatusRequest(content_id="resource_abc", status=False)
    response = await handler.handle(request)

    assert response.is_success is True
    assert response.new_status is False
    assert response.content_id == "resource_abc"
    content_repository.update_resource_status.assert_called_once_with(
        content_id="resource_abc", new_status=False
    )
