from src.provider.user_config_provider import UserConfigProvider


class GetAlert:
    __user_config_provider: UserConfigProvider

    def __init__(self):
        self.__user_config_provider = UserConfigProvider()

    def enact(self, event: dict):
        raise NotImplementedError('Get alert by id not yet implemented')
