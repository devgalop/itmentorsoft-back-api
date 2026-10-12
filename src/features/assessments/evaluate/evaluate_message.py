import json
from common_py_aws import PublishMessageRequest
from itmentorsoft_persistence.dto import Assessment

from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants


class EvaluateMessage(PublishMessageRequest):
    def __init__(self, assessment: Assessment):
        self.assessment = assessment

    def get_url(self) -> str:
        return EnvironmentVariablesConstants.AWS_SQS_QUALIFICATION_QUEUE_URL

    def get_message(self) -> str:
        """Retrieve the serialized assessment message to be published.

        Returns:
            str: The serialized assessment message.
        """
        assessment_dict = {
            "assessment_id": self.assessment.assessment_id,
            "user_id": self.assessment.user_id,
            "created_at": self.assessment.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
            "answers": [
                {
                    "answer_id": answer.answer_id,
                    "question_id": answer.question_id,
                    "assessment_id": answer.assessment_id,
                    "answer": answer.answer,
                    "time_taken_seconds": answer.time_taken_seconds,
                }
                for answer in self.assessment.answers
            ],
        }

        return json.dumps(assessment_dict)
