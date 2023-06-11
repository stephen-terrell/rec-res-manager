from typing import List

from src.provider.user_config_provider import UserConfigProvider


class ListNotifications:
    def __init__(self, event: dict):
        self.__user_config_provider: UserConfigProvider = UserConfigProvider()

        self.__user_id: str = event["headers"]["x-rec-res-user-id"]

    def enact(self) -> List[dict]:
        user_config: dict = self.__user_config_provider.get_v2_user_config()

        if user_config is None or "userConfigs" not in user_config or self.__user_id not in user_config["userConfigs"]:
            return []

        user_notification_configs: dict = user_config["userConfigs"][self.__user_id]["alertSubscriptions"]

        result: List = [
            {
                "notificationId": key,
                "protocol": value["protocol"],
                "endpoint": value["endpoint"],
            }
            for key, value in user_notification_configs.items()
        ]

        return result
