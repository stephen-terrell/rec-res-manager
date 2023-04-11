import os
import json

import boto3


class SqsProxy:
    __api_command_queue_url: str = None
    __api_command_queue = None

    def __init__(self):
        self.__api_command_queue_url = os.environ['API_COMMAND_QUEUE_URL']
        sqs_resource = boto3.resource('sqs')
        self.__api_command_queue = sqs_resource.Queue(self.__api_command_queue_url)

    def send_api_command(self, message: dict):
        self.__api_command_queue.send_message(
            MessageBody=json.dumps(message)
        )
