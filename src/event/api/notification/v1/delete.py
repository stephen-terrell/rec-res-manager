from src.proxy.sqs_proxy import SqsProxy


class DeleteNotification:
    def __init__(self, event: dict):
        self.__sqs_proxy: SqsProxy = SqsProxy()

        self.__message = {
            "commandName": "DELETE_NOTIFICATION",
            "data": {
                "userId": event["headers"]["x-rec-res-user-id"],
                "notificationId": event["pathParameters"]["notificationId"],
            },
        }

    def enact(self):
        self.__sqs_proxy.send_api_command(self.__message)
