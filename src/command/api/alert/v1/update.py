from src.command.api.alert.v1.create import CreateAlert

class UpdateAlert:

    def __init__(self):
        pass

    @staticmethod
    def generate_command(event: dict):
        raise NotImplementedError()

    @staticmethod
    def handle_command(user_config: dict, message: dict) -> dict:
        return CreateAlert.handle_command(user_config, message)
