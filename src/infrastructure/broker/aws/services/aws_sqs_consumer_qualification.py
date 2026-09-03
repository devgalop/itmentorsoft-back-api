import json
from src.features.assessments.evaluate.evaluate_assessment_contract import (
    EvaluateAssessmentContract,
)
from src.features.assessments.evaluate.evaluate_assessment_request import (
    EvaluateAssessmentRequest,
)
from itmentorsoft_persistence.dto import Assessment, AssessmentAnswer
from src.infrastructure.broker.aws.models.aws_sqs_messages import SqsMessageReceived
from src.infrastructure.broker.aws.services.aws_sqs_connection_factory import (
    SqsConnection,
)
from src.infrastructure.broker.aws.services.aws_sqs_consumer_service import (
    SqsConsumerService,
)
from src.infrastructure.broker.aws.models.aws_sqs_consumer_config import (
    SqsConsumerConfig,
)


class SqsConsumerQualification(SqsConsumerService):
    def __init__(
        self,
        sqs_config: SqsConsumerConfig,
        sqs_client: SqsConnection,
        evaluate_contract: EvaluateAssessmentContract,
    ):
        super().__init__(sqs_client, sqs_config)
        self.evaluate_contract = evaluate_contract

    async def process_message(self, message: SqsMessageReceived) -> bool:
        try:
            assessment_read = json.loads(message.body)
            answers = [
                AssessmentAnswer(
                    answer_id=answer["answer_id"],
                    assessment_id=answer["assessment_id"],
                    question_id=answer["question_id"],
                    answer=answer["answer"],
                    time_taken_seconds=answer["time_taken_seconds"],
                )
                for answer in assessment_read["answers"]
            ]
            assessment = Assessment(
                assessment_id=assessment_read["assessment_id"],
                user_id=assessment_read["user_id"],
                created_at=assessment_read["created_at"],
                answers=answers,
            )
            print(
                f"Processing message {message.message_id} with assessment: {assessment}"
            )
            result = await self.evaluate_contract.evaluate(
                EvaluateAssessmentRequest(assessment=assessment)
            )
            return result.is_success
        except Exception as e:
            print(f"Error processing message {message.message_id}: {e}")
            return False
