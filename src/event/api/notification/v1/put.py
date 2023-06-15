from uuid import uuid4

from src.proxy.sqs_proxy import SqsProxy


class PutNotification:
    def __init__(self, event: dict):
        self.__sqs_proxy: SqsProxy = SqsProxy()

        self.__message = {
            "commandName": "CREATE_NOTIFICATION",
            "data": {
                "userId": event["headers"]["x-rec-res-user-id"],
                "notificationId": str(uuid4()),
                "protocol": "email",
                "endpoint": event["body"]["endpoint"],
            },
        }

    def enact(self) -> dict:
        self.__sqs_proxy.send_api_command(self.__message)

        return self.__message["data"]  # type: ignore
