from typing import List

from src.provider.user_config_provider import UserConfigProvider


class ListAlerts:
    def __init__(self, event: dict):
        self.__user_config_provider: UserConfigProvider = UserConfigProvider()

        self.__user_id: str = event["headers"]["x-rec-res-user-id"]

    def enact(self) -> List[dict]:
        user_config = self.__user_config_provider.get_v2_user_config()

        if user_config is None or "userConfigs" not in user_config or self.__user_id not in user_config["userConfigs"]:
            return []

        user_alert_configs: dict = user_config["userConfigs"][self.__user_id]["alertConfigs"]

        result: List = [
            {
                "userId": self.__user_id,
                "alertId": key,
                "type": value["type"],
                "campgroundId": value["campgroundId"],
                "checkInDate": value["checkInDate"],
                "checkOutDate": value["checkOutDate"],
                "notificationPreferences": {
                    "notificationSensitivityLevel": value["notificationPreferences"]["notificationSensitivityLevel"],
                    "notificationsEnabled": value["notificationPreferences"]["notificationsEnabled"],
                },
            }
            for key, value in user_alert_configs.items()
        ]

        return result
