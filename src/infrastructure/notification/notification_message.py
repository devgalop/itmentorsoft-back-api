import json

from common_py_aws import PublishMessageRequest

from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants


class QuestionCreatedNotifyRequest:
    def __init__(
        self,
        recipient: str,
        reviewer: str,
        owner: str,
        object_name: str,
        object_code: str,
        created_at: str,
        url_review: str,
    ):
        self.recipient = recipient
        self.reviewer = reviewer
        self.owner = owner
        self.object_name = object_name
        self.object_code = object_code
        self.created_at = created_at
        self.url_review = url_review


class OtpNotifyRequest:
    def __init__(self, recipient: str, user: str, otp_code: str, expiration: str):
        self.recipient = recipient
        self.user = user
        self.otp_code = otp_code
        self.expiration = expiration


class RecoverPasswordNotifyRequest:
    def __init__(
        self, recipient: str, url_base: str, url_token: str, user: str, id_trx: str
    ):
        self.recipient = recipient
        self.url_base = url_base
        self.url_token = url_token
        self.user = user
        self.id_trx = id_trx


class UserCreatedNotifyRequest:
    def __init__(
        self, recipient: str, user: str, role: str, created_at: str, login_url: str
    ):
        self.recipient = recipient
        self.user = user
        self.role = role
        self.created_at = created_at
        self.login_url = login_url


class NotificationResponse:
    def __init__(self, is_success: bool, message: str):
        self.is_success = is_success
        self.message = message


class NotificationMessageVariables:
    def __init__(self, key: str, value: str):
        self.key = key
        self.value = value

    def to_dict(self) -> dict[str, str]:
        return {"key": self.key, "value": self.value}

    def to_json(self) -> str:
        return json.dumps(self.to_dict())


class NotificationMessage(PublishMessageRequest):

    def __init__(
        self,
        recipient: str,
        subject: str,
        html_template_code: str,
        message_variables: list[NotificationMessageVariables],
    ):
        self.recipient = recipient
        self.subject = subject
        self.html_template_code = html_template_code
        self.message_variables = message_variables

    def get_url(self) -> str:
        return EnvironmentVariablesConstants.AWS_SQS_NOTIFY_QUEUE_URL

    def get_message(self) -> str:
        return self.to_json()

    def to_dict(self) -> dict[str, str | list[dict[str, str]]]:
        return {
            "recipient": self.recipient,
            "subject": self.subject,
            "html_template_code": self.html_template_code,
            "message_variables": [mv.to_dict() for mv in self.message_variables],
        }

    def to_json(self) -> str:
        return json.dumps(self.to_dict())
