from src.features.assessments.evaluate.evaluate_assessment_contract import (
    EvaluateAssessmentContract,
)
from src.infrastructure.broker.aws.models.aws_sqs_client import SqsConnectionRequest
from src.infrastructure.broker.aws.models.aws_sqs_consumer_config import (
    SqsConsumerConfig,
)
from src.infrastructure.broker.aws.services.aws_sqs_connection_factory import (
    SqsConnectionFactoryService,
)
from src.infrastructure.broker.aws.services.aws_sqs_consumer_qualification import (
    SqsConsumerQualification,
)
from src.infrastructure.broker.aws.services.aws_sqs_consumer_service import (
    SqsConsumerService,
)
from src.infrastructure.broker.aws.services.aws_sqs_creator_service import (
    SqsCreatorService,
)
from src.infrastructure.env_manager.env_manager import EnvironmentVariablesConstants


class SqsManagerService:
    def __init__(self, evaluate_contract: EvaluateAssessmentContract):
        self.evaluate_contract = evaluate_contract

    def create_connection_factory(self) -> SqsConnectionFactoryService:
        """Create an SQS connection using the provided configuration.

        Returns:
            SqsConnectionFactoryService: An instance of the SqsConnectionFactoryService.
        """
        sqs_connection_factory = SqsConnectionFactoryService(
            connection_request=SqsConnectionRequest(
                endpoint_url=EnvironmentVariablesConstants.AWS_ENDPOINT_URL,
                access_key=EnvironmentVariablesConstants.AWS_ACCESS_KEY_ID,
                secret_key=EnvironmentVariablesConstants.AWS_SECRET_ACCESS_KEY,
                region=EnvironmentVariablesConstants.AWS_REGION,
            )
        )
        return sqs_connection_factory

    def create_queues(self):
        sqs_connection_factory = self.create_connection_factory()
        sqs_connection = sqs_connection_factory.create_connection()
        sqs_creator_service = SqsCreatorService(sqs_connection)
        sqs_creator_service.create_queue("mq-itmentorsoft-qualify-001")

    def start_consumer_services(self) -> dict[str, SqsConsumerService]:
        # Initialize the SQS connection and configuration
        sqs_config_qualification = SqsConsumerConfig(
            queue_url=EnvironmentVariablesConstants.AWS_SQS_QUALIFICATION_QUEUE_URL,
            max_messages=10,
            wait_time_seconds=20,
            is_enabled=True,
        )
        sqs_connection_factory = self.create_connection_factory()

        # Create an instance of the SqsConsumerQualification service
        sqs_connection = sqs_connection_factory.create_connection()
        sqs_consumer_qualification_service = SqsConsumerQualification(
            sqs_config_qualification, sqs_connection, self.evaluate_contract
        )

        # Start the consumer service
        sqs_consumer_qualification_service.start_consumer()

        return {
            "qualification": sqs_consumer_qualification_service,
        }

    async def stop_consumer_services(
        self, consumer_services: dict[str, SqsConsumerService]
    ):
        for service_name, consumer_service in consumer_services.items():
            print(f"Stopping {service_name} consumer service...")
            await consumer_service.stop_consumer()
            print(f"{service_name} consumer service stopped.")
