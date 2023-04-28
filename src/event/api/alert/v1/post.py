from src.proxy.sqs_proxy import SqsProxy


class PostAlert:
    __sqs_proxy: SqsProxy = None

    def __init__(self, event: dict):
        self.__sqs_proxy = SqsProxy()

        self.__message = {
            'commandName': 'UPDATE_ALERT',
            'data': {
                'userId': event['headers']['x-rec-res-user-id'],
                'alertId': event['pathParameters']['alertId'],
                'type': 'recreation.gov',
                'checkInDate': event['body']['checkInDate'],
                'checkOutDate': event['body']['checkOutDate'],
                'notificationPreferences': {
                    'notificationSensitivityLevel':
                        event['body']['notificationPreferences']['notificationSensitivityLevel'],
                    'notificationsEnabled':
                        event['body']['notificationPreferences']['notificationsEnabled'],
                },
            }
        }

    def enact(self):
        self.__sqs_proxy.send_api_command(self.__message)

        return self.__message['data']
