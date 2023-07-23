from typing import List

from src.proxy.sns_proxy import SnsProxy


class ListNotifications:
    def __init__(self, event: dict):
        self.__sns_proxy: SnsProxy = SnsProxy()

        self.__user_id: str = event["headers"]["x-rec-res-user-id"]

    def enact(self) -> List[dict]:
        if not self.__sns_proxy.topic_exists(self.__user_id):
            self.__sns_proxy.create_topic(self.__user_id)

        topic_subscriptions = self.__sns_proxy.list_subscriptions(self.__user_id)

        return [
            {
                "notificationId": sub["SubscriptionArn"].split(":")[-1],
                "protocol": sub["Protocol"],
                "endpoint": sub["Endpoint"],
            }
            for sub in topic_subscriptions
            if sub["SubscriptionArn"] != "PendingConfirmation"
        ]
