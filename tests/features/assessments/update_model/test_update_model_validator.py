import pytest

from src.features.assessments.update_model.update_model_request import (
    UpdateModelRequest,
)


def test_when_request_is_valid_should_not_raise_exception():
    request = UpdateModelRequest(process="qualifier", model_id="model-123")
    assert request.process == "qualifier"
    assert request.model_id == "model-123"


def test_when_process_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="Process cannot be empty"):
        UpdateModelRequest(process="", model_id="model-123")


def test_when_process_is_too_short_should_raise_exception():
    with pytest.raises(ValueError, match="Process must be at least 3 characters long"):
        UpdateModelRequest(process="ab", model_id="model-123")


def test_when_process_is_too_long_should_raise_exception():
    long_process = "a" * 51
    with pytest.raises(ValueError, match="Process cannot exceed 50 characters"):
        UpdateModelRequest(process=long_process, model_id="model-123")


def test_when_model_id_is_empty_should_raise_exception():
    with pytest.raises(ValueError, match="Model ID cannot be empty"):
        UpdateModelRequest(process="qualifier", model_id="")


def test_when_model_id_is_too_short_should_raise_exception():
    with pytest.raises(ValueError, match="Model ID must be at least 5 characters long"):
        UpdateModelRequest(process="qualifier", model_id="abcd")


def test_when_model_id_is_too_long_should_raise_exception():
    long_model_id = "a" * 21
    with pytest.raises(ValueError, match="Model ID cannot exceed 20 characters"):
        UpdateModelRequest(process="qualifier", model_id=long_model_id)


def test_when_process_is_at_minimum_length_should_not_raise():
    request = UpdateModelRequest(process="abc", model_id="model-123")
    assert request.process == "abc"


def test_when_process_is_at_maximum_length_should_not_raise():
    max_process = "a" * 50
    request = UpdateModelRequest(process=max_process, model_id="model-123")
    assert request.process == max_process


def test_when_model_id_is_at_minimum_length_should_not_raise():
    request = UpdateModelRequest(process="qualifier", model_id="abcde")
    assert request.model_id == "abcde"


def test_when_model_id_is_at_maximum_length_should_not_raise():
    max_model_id = "a" * 20
    request = UpdateModelRequest(process="qualifier", model_id=max_model_id)
    assert request.model_id == max_model_id
