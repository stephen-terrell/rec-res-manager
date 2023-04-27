import pytest

from src.command.api.alert.v1.create import CreateAlert


class TestCreate:

    @pytest.fixture
    def user_config(self):
        return {
            'userConfigs': {}
        }

    @pytest.fixture
    def user_id(self):
        return 'user-1234'

    @pytest.fixture
    def alert_id(self):
        return 'alert-4321'

    @pytest.fixture
    def config(self):
        return {
            'type': 'recreation.gov',
            'campgroundId': 'oifnweoifnw',
            'checkInDate': '01/01/2020',
            'checkOutDate': '01/01/2020',
            'notificationPreferences': {
                'notificationSensitivityLevel':
                   'asdf',
                'notificationsEnabled':
                    'asdf',
            },
        }

    @pytest.fixture
    def message(self, user_id, alert_id, config):
        return {
            'userId': user_id,
            'alertId': alert_id,
            **config,
        }

    def test_handle_command(self, user_config, message, config, user_id, alert_id):
        result = CreateAlert.handle_command(user_config, message)

        assert result == {
            'userConfigs': {
                user_id: {
                    'version': 1,
                    'alertSubscriptions': [],
                    'alertConfigs': {
                        alert_id: config,
                    },
                },
            },
        }
