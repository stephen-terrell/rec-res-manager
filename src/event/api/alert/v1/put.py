from uuid import uuid4

from src.proxy.sqs_proxy import SqsProxy


class PutAlert:
    __sqs_proxy: SqsProxy = None

    def __init__(self, event: dict):
        self.__sqs_proxy = SqsProxy()

        self.__message = {
            'commandName': 'CREATE_ALERT',
            'data': {
                'userId': event['headers']['x-rec-res-user-id'],
                'alertId': str(uuid4()),
                'type': 'recreation.gov',
                'campgroundId': event['body']['campgroundId'],
                'checkInDate': event['body']['checkInDate'],
                'checkOutDate': event['body']['checkOutDate'],
                'notificationPreferences': {
                    'notificationSensitivityLevel':
                        event['body']['notificationPreferences']['notificationSensitivityLevel'],
                    'notificationsEnabled': True,
                }
            }
        }

    def enact(self) -> dict:
        self.__sqs_proxy.send_api_command(self.__message)

        return self.__message['data']
