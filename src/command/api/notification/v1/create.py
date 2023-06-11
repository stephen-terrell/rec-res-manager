class CreateNotification:
    @staticmethod
    def generate_command(event: dict):
        raise NotImplementedError()

    @staticmethod
    def handle_command(user_config: dict, message: dict) -> dict:
        user_id = message["userId"]

        # TODO: encapsulate (used in alerts too)
        if user_id not in user_config["userConfigs"]:
            user_config["userConfigs"][user_id] = {
                "version": 1,
                "alertSubscriptions": {},
                "alertConfigs": {},
            }

        user_config["userConfigs"][user_id]["alertSubscriptions"][message["notificationId"]] = {
            "protocol": message["protocol"],
            "endpoint": message["endpoint"],
        }

        return user_config
