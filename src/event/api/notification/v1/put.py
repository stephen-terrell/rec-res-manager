from src.model.enum.protocol_type import ProtocolType
from src.model.subscription_config import SubscriptionConfig
from src.proxy.sns_proxy import SnsProxy


class PutNotification:
    def __init__(self, event: dict):
        self.__event: dict = event
        self.__sns_proxy: SnsProxy = SnsProxy()

    def enact(self) -> dict:
        user_id = self.__event["headers"]["x-rec-res-user-id"]
        if not self.__sns_proxy.topic_exists(user_id):
            self.__sns_proxy.create_topic(user_id)

        endpoint = self.__event["body"]["endpoint"]
        subscription_id = self.__sns_proxy.create_subscription(
            user_id, SubscriptionConfig(endpoint, ProtocolType.EMAIL)
        )

        return {"userId": user_id, "notificationId": subscription_id, "protocol": "email", "endpoint": endpoint}
