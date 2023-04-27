

class DeleteAlert:

    def __init__(self):
        pass

    @staticmethod
    def generate_command(event: dict):
        raise NotImplementedError()

    @staticmethod
    def handle_command(user_config: dict, message: dict) -> dict:
        user_id = message['userId']
        if user_id in user_config['userConfigs']:
            user_config['userConfigs'][user_id]['alertConfigs'].pop(message['alertId'], None)

        return user_config
