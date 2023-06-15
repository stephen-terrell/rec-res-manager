import pytest

from src.command.api.notification.v1.create import CreateNotification


class TestCreate:
    @pytest.fixture
    def user_config(self):
        return {"userConfigs": {}}

    @pytest.fixture
    def user_id(self):
        return "user-1234"

    @pytest.fixture
    def notification_id(self):
        return "454545454"

    @pytest.fixture
    def endpoint(self):
        return "test@test.com"

    @pytest.fixture
    def message(self, user_id, notification_id, endpoint):
        return {"userId": user_id, "notificationId": notification_id, "protocol": "email", "endpoint": endpoint}

    def test_generate_command(self):
        with pytest.raises(NotImplementedError):
            CreateNotification.generate_command({})

    def test_handle_command_user_exists(self, user_config, user_id, message, notification_id, endpoint):
        user_config["userConfigs"][user_id] = {
            "version": 1,
            "alertSubscriptions": {},
            "alertConfigs": {},
        }

        result = CreateNotification.handle_command(user_config, message)

        assert result == {
            "userConfigs": {
                user_id: {
                    "version": 1,
                    "alertSubscriptions": {
                        notification_id: {
                            "protocol": "email",
                            "endpoint": endpoint,
                        },
                    },
                    "alertConfigs": {},
                },
            },
        }

    def test_handle_command_user_not_exists(self, user_config, user_id, message, notification_id, endpoint):
        result = CreateNotification.handle_command(user_config, message)

        assert result == {
            "userConfigs": {
                user_id: {
                    "version": 1,
                    "alertSubscriptions": {
                        notification_id: {
                            "protocol": "email",
                            "endpoint": endpoint,
                        },
                    },
                    "alertConfigs": {},
                },
            },
        }
