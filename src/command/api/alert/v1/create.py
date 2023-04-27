

class CreateAlert:

    def __init__(self):
        pass

    @staticmethod
    def generate_command(event: dict):
        raise NotImplementedError()

    @staticmethod
    def handle_command(user_config: dict, message: dict) -> dict:
        user_id = message['userId']
        if user_id not in user_config['userConfigs']:
            user_config['userConfigs'][user_id] = {
                'version': 1,
                'alertSubscriptions': [],
                'alertConfigs': {},
            }

        user_config['userConfigs'][user_id]['alertConfigs'][message['alertId']] = {
            'type': 'recreation.gov',
            'campgroundId': message['campgroundId'],
            'checkInDate': message['checkInDate'],
            'checkOutDate': message['checkOutDate'],
            'notificationPreferences': {
                'notificationSensitivityLevel':
                    message['notificationPreferences']['notificationSensitivityLevel'],
                'notificationsEnabled':
                    message['notificationPreferences']['notificationsEnabled'],
            },
        }

        return user_config
