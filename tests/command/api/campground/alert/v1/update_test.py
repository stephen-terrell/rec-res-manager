import pytest

from src.command.api.campground.alert.v1.update import UpdateAlert


class TestUpdate:
    @pytest.fixture
    def user_config(self, user_id, alert_id):
        return {
            "userConfigs": {
                user_id: {
                    "version": 1,
                    "alertSubscriptions": [],
                    "alertConfigs": {
                        alert_id: {
                            "type": "recreation.gov",
                            "campgroundId": "1234",
                            "checkInDate": "01/01/2020",
                            "checkOutDate": "01/01/2020",
                            "notificationPreferences": {
                                "notificationSensitivityLevel": "asdf",
                                "notificationsEnabled": "asdf",
                            },
                        },
                    },
                }
            }
        }

    @pytest.fixture
    def user_id(self):
        return "user-1234"

    @pytest.fixture
    def alert_id(self):
        return "alert-4321"

    @pytest.fixture
    def update_config(self):
        return {
            "type": "recreation.gov",
            "campgroundId": "777777777",
            "checkInDate": "01/01/2022",
            "checkOutDate": "01/01/2022",
            "notificationPreferences": {
                "notificationSensitivityLevel": "fdsa",
                "notificationsEnabled": "fdsa",
            },
        }

    @pytest.fixture
    def message(self, user_id, alert_id, update_config):
        return {
            "userId": user_id,
            "alertId": alert_id,
            **update_config,
        }

    def test_generate_command(self):
        with pytest.raises(NotImplementedError):
            UpdateAlert.generate_command({})

    def test_handle_command(self, user_config, message, update_config, user_id, alert_id):
        result = UpdateAlert.handle_command(user_config, message)

        assert result == {
            "userConfigs": {
                user_id: {
                    "version": 1,
                    "alertSubscriptions": [],
                    "alertConfigs": {alert_id: {**update_config, "campgroundId": "1234"}},
                },
            },
        }
