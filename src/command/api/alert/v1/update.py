class UpdateAlert:
    def __init__(self):
        pass

    @staticmethod
    def generate_command(event: dict):
        raise NotImplementedError()

    @staticmethod
    def handle_command(user_config: dict, message: dict) -> dict:
        user_config["userConfigs"][message["userId"]]["alertConfigs"][message["alertId"]] = {
            "type": "recreation.gov",
            "campgroundId": user_config["userConfigs"][message["userId"]]["alertConfigs"][message["alertId"]][
                "campgroundId"
            ],
            "checkInDate": message["checkInDate"],
            "checkOutDate": message["checkOutDate"],
            "notificationPreferences": {
                "notificationSensitivityLevel": message["notificationPreferences"]["notificationSensitivityLevel"],
                "notificationsEnabled": message["notificationPreferences"]["notificationsEnabled"],
            },
        }

        return user_config
