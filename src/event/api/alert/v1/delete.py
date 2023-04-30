from src.proxy.sqs_proxy import SqsProxy


class DeleteAlert:
    def __init__(self, event: dict):
        self.__sqs_proxy: SqsProxy = SqsProxy()

        self.__message = {
            "commandName": "DELETE_ALERT",
            "data": {
                "userId": event["headers"]["x-rec-res-user-id"],
                "alertId": event["pathParameters"]["alertId"],
            },
        }

    def enact(self):
        self.__sqs_proxy.send_api_command(self.__message)
