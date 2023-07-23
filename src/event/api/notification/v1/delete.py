from src.proxy.sns_proxy import SnsProxy


class DeleteNotification:
    def __init__(self, event: dict):
        self.__event: dict = event
        self.__sns_proxy: SnsProxy = SnsProxy()

    def enact(self):
        user_id = self.__event["headers"]["x-rec-res-user-id"]
        subscription_id = self.__event["pathParameters"]["notificationId"]

        self.__sns_proxy.remove_subscription(user_id, subscription_id)
