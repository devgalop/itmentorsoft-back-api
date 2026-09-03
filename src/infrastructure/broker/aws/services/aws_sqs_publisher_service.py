from src.features.shared.publisher_service import (
    PublishMessageRequest,
    PublishMessageResponse,
    PublisherService,
)
from src.infrastructure.broker.aws.services.aws_sqs_connection_factory import (
    SqsConnection,
)
from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants


class SqsPublishMessageRequest:
    def __init__(self, queue_url: str, message: str):
        self.queue_url = queue_url
        self.message = message


class SqsPublisherService:
    def __init__(self, sqs_client: SqsConnection):
        self.sqs_client = sqs_client

    def publish(self, request: SqsPublishMessageRequest) -> bool:
        """Publish a message to the specified SQS queue.

        Args:
            request (SqsPublishMessageRequest): The request containing the queue URL and message.

        Returns:
            bool: The result of the publish operation.
        """

        response = self.sqs_client.client.send_message(
            QueueUrl=request.queue_url, MessageBody=request.message
        )
        if response.get("ResponseMetadata", {}).get("HTTPStatusCode") != 200:
            return False

        return True


class EvaluateAssessmentPublishAdapter(PublisherService):

    def __init__(self, sqs_client: SqsConnection):
        self.sqs_client = sqs_client

    async def publish(self, request: PublishMessageRequest) -> PublishMessageResponse:
        """Publish a message to the specified SQS queue.

        Args:
            request (PublishMessageRequest): The request containing the queue URL and message.

        Returns:
            PublishMessageResponse: The result of the publish operation.
        """
        try:
            sqs_service = SqsPublisherService(sqs_client=self.sqs_client)
            response = sqs_service.publish(
                request=SqsPublishMessageRequest(
                    queue_url=EnvironmentVariablesConstants.AWS_SQS_QUALIFICATION_QUEUE_URL,
                    message=request.get_message(),
                )
            )

            if not response:
                return PublishMessageResponse(
                    success=False, message="Failed to publish message."
                )

            return PublishMessageResponse(
                success=True, message="Message published successfully."
            )

        except Exception as e:
            return PublishMessageResponse(success=False, message=str(e))


class ClassificateStudentPublishAdapter(PublisherService):

    def __init__(self, sqs_client: SqsConnection):
        self.sqs_client = sqs_client

    async def publish(self, request: PublishMessageRequest) -> PublishMessageResponse:
        """Publish a message to the specified SQS queue.

        Args:
            request (PublishMessageRequest): The request containing the queue URL and message.

        Returns:
            PublishMessageResponse: The result of the publish operation.
        """
        try:
            sqs_service = SqsPublisherService(sqs_client=self.sqs_client)
            response = sqs_service.publish(
                request=SqsPublishMessageRequest(
                    queue_url=EnvironmentVariablesConstants.AWS_SQS_CLASSIFICATION_QUEUE_URL,
                    message=request.get_message(),
                )
            )

            if not response:
                return PublishMessageResponse(
                    success=False, message="Failed to publish message."
                )

            return PublishMessageResponse(
                success=True, message="Message published successfully."
            )

        except Exception as e:
            return PublishMessageResponse(success=False, message=str(e))
