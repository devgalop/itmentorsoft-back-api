import asyncio
from abc import ABC, abstractmethod
from src.infrastructure.broker.aws.models.aws_sqs_consumer_config import (
    SqsConsumerConfig,
)
from src.infrastructure.broker.aws.models.aws_sqs_messages import SqsMessageReceived
from src.infrastructure.broker.aws.services.aws_sqs_connection_factory import (
    SqsConnection,
)


class SqsConsumerService(ABC):
    def __init__(self, sqs_client: SqsConnection, sqs_config: SqsConsumerConfig):
        self.sqs_client = sqs_client
        self.sqs_config = sqs_config
        self._task: asyncio.Task | None = None
        self._stopping = False

    def start_consumer(self):
        self._stopping = False
        self._task = asyncio.create_task(self._consume_messages())

    async def _consume_messages(self):
        while not self._stopping:
            if not self.sqs_config.is_enabled:
                await asyncio.sleep(30)
                continue

            try:
                messages = await asyncio.to_thread(
                    self.sqs_client.client.receive_message,
                    QueueUrl=self.sqs_config.queue_url,
                    MaxNumberOfMessages=self.sqs_config.max_messages,
                    WaitTimeSeconds=self.sqs_config.wait_time_seconds,
                    AttributeNames=["ApproximateReceiveCount"],
                )
                if not messages or "Messages" not in messages:
                    await asyncio.sleep(30)
                    continue
                messages_recieved: list[SqsMessageReceived] = []
                for message in messages.get("Messages", []):
                    message_recieved = SqsMessageReceived(
                        message_id=message["MessageId"],
                        body=message["Body"],
                        receipt_handle=message["ReceiptHandle"],
                        retry_count=int(
                            message["Attributes"].get("ApproximateReceiveCount", 0)
                        ),
                    )
                    messages_recieved.append(message_recieved)
                    self.sqs_client.client.change_message_visibility(
                        QueueUrl=self.sqs_config.queue_url,
                        ReceiptHandle=message_recieved.receipt_handle,
                        VisibilityTimeout=200,
                    )

                print(f"Received {len(messages_recieved)} messages")
                for message_recieved in messages_recieved:
                    result = await self.process_message(message_recieved)
                    if result:
                        await asyncio.to_thread(
                            self.sqs_client.client.delete_message,
                            QueueUrl=self.sqs_config.queue_url,
                            ReceiptHandle=message_recieved.receipt_handle,
                        )
                        print(f"Deleted message: {message_recieved.message_id}")
            except Exception as e:
                print(f"Error processing messages: {e}")
            await asyncio.sleep(30)

    @abstractmethod
    async def process_message(self, message: SqsMessageReceived) -> bool:
        pass

    async def stop_consumer(self):
        self._stopping = True
        if self._task is not None:
            self._task.cancel()
        try:
            if self._task is not None:
                await self._task
        except asyncio.CancelledError:
            pass
