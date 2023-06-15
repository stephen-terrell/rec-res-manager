import pytest

from src.command.api.notification.v1.delete import DeleteNotification


class TestDelete:
    @pytest.fixture
    def user_id(self):
        return "user-1234"

    @pytest.fixture
    def notification_id(self):
        return "hfhfhfhf"

    @pytest.fixture
    def user_config(self, user_id, notification_id):
        return {
            "userConfigs": {
                user_id: {
                    "alertSubscriptions": {notification_id: {"asdf": "asdf,"}},
                },
            },
        }

    def test_generate_command(self):
        with pytest.raises(NotImplementedError):
            DeleteNotification.generate_command({})

    def test_handle_command_user_not_exist(self, user_id, notification_id, user_config):
        user_config["userConfigs"].pop(user_id)

        result = DeleteNotification.handle_command(user_config, {"userId": user_id, "notificationId": notification_id})

        assert user_id not in result["userConfigs"]

    def test_handle_command_user_exists(self, user_id, notification_id, user_config):
        result = DeleteNotification.handle_command(user_config, {"userId": user_id, "notificationId": notification_id})

        assert notification_id not in result["userConfigs"][user_id]["alertSubscriptions"]
