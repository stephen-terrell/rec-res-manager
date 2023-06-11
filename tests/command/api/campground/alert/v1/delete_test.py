import pytest

from src.command.api.campground.alert.v1.delete import DeleteAlert


class TestDelete:
    @pytest.fixture
    def user_id(self):
        return "user-1234"

    @pytest.fixture
    def alert_id(self):
        return "alert-1234"

    @pytest.fixture
    def user_config(self, user_id, alert_id):
        return {"userConfigs": {user_id: {"alertConfigs": {alert_id: {"asdf": "asdf"}}}}}

    def test_generate_command(self):
        with pytest.raises(NotImplementedError):
            DeleteAlert.generate_command({})

    def test_handle_command_user_not_exist(self, user_id, alert_id, user_config):
        user_config["userConfigs"].pop(user_id)

        result = DeleteAlert.handle_command(user_config, {"userId": user_id, "alertId": alert_id})

        assert user_id not in result["userConfigs"]

    def test_handle_command_user_exists(self, user_id, alert_id, user_config):
        result = DeleteAlert.handle_command(user_config, {"userId": user_id, "alertId": alert_id})

        assert alert_id not in result["userConfigs"][user_id]["alertConfigs"]
