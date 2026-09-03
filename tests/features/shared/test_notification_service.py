from unittest.mock import patch

from src.features.shared.notification_service import (
    NotificationConfigBuilder,
)


def test_add_attachment_appends_file_to_attachments_list():
    builder = NotificationConfigBuilder("dest@example.com", "Subject")
    builder.add_attachment("report.pdf")
    config = builder.build()
    assert config.attachments == ["report.pdf"]


def test_add_multiple_attachments_appends_all_to_list():
    builder = NotificationConfigBuilder("dest@example.com", "Subject")
    builder.add_attachment("report.pdf").add_attachment("summary.pdf")
    config = builder.build()
    assert len(config.attachments) == 2
    assert config.attachments == ["report.pdf", "summary.pdf"]


def test_add_attachment_returns_builder_for_chaining():
    builder = NotificationConfigBuilder("dest@example.com", "Subject")
    result = builder.add_attachment("file.pdf")
    assert result is builder


def test_set_template_assigns_template_to_config():
    builder = NotificationConfigBuilder("dest@example.com", "Subject")
    builder.set_template("<html>Hello</html>")
    config = builder.build()
    assert config.template == "<html>Hello</html>"


def test_notification_config_builder_full_chain():
    with patch(
        "src.features.shared.notification_service.EnvironmentVariablesConstants.EMAIL_DEFAULT_SENDER",
        "sender@example.com",
    ):
        config = (
            NotificationConfigBuilder("dest@example.com", "Welcome")
            .set_template("<html>Hello</html>")
            .add_attachment("report.pdf")
            .build()
        )
    assert config.sender == "sender@example.com"
    assert config.destination == "dest@example.com"
    assert config.subject == "Welcome"
    assert config.template == "<html>Hello</html>"
    assert config.attachments == ["report.pdf"]
