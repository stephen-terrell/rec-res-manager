from src.provider.user_config_provider import UserConfigProvider


class GetAlert:
    __user_config_provider: UserConfigProvider

    def __init__(self, event: dict):
        pass

    def enact(self):
        raise NotImplementedError('Get alert by id not yet implemented')
