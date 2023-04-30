import os
import json
from typing import List

import boto3


class SqsProxy:
    def __init__(self):
        self.__api_command_queue_url = os.environ["API_COMMAND_QUEUE_URL"]
        self.__sqs_client = boto3.client("sqs")
        self.__message_group_id = "rec-res-api-commands"

    def send_api_command(self, message: dict):
        self.__sqs_client.send_message(
            QueueUrl=self.__api_command_queue_url,
            MessageBody=json.dumps(message),
            MessageGroupId=self.__message_group_id,
        )

    def delete_api_command_messages(self, receipt_handles: List[str]):
        entries = [{"Id": str(index), "ReceiptHandle": handle} for index, handle in enumerate(receipt_handles)]
        self.__sqs_client.delete_message_batch(
            QueueUrl=self.__api_command_queue_url,
            Entries=entries,
        )
