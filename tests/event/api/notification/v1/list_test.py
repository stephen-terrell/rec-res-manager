import pytest
from unittest.mock import patch

from src.event.api.notification.v1.list import ListNotifications


class TestList:
    @pytest.fixture
    def user_id_1(self):
        return "stephen"

    @pytest.fixture
    def user_id_2(self):
        return "other"

    @pytest.fixture
    def make_event(self):
        def _make_event(user_id):
            return {"headers": {"x-rec-res-user-id": user_id}}

        return _make_event

    @pytest.fixture
    def notification_id_1(self):
        return "id-1"

    @pytest.fixture
    def notification_id_2(self):
        return "id-2"

    @pytest.fixture
    def notification_id_3(self):
        return "id-3"

    @pytest.fixture
    def endpoint_1(self):
        return "111111111"

    @pytest.fixture
    def endpoint_2(self):
        return "222222222"

    @pytest.fixture
    def endpoint_3(self):
        return "333333333"

    @pytest.fixture
    def user_config(
        self,
        user_id_1,
        user_id_2,
        notification_id_1,
        notification_id_2,
        notification_id_3,
        endpoint_1,
        endpoint_2,
        endpoint_3,
    ):
        return {
            "userConfigs": {
                user_id_1: {
                    "version": 1,
                    "alertSubscriptions": {
                        notification_id_1: {
                            "endpoint": endpoint_1,
                            "protocol": "email",
                        }
                    },
                    "alertConfigs": {},
                },
                user_id_2: {
                    "version": 1,
                    "alertSubscriptions": {
                        notification_id_2: {
                            "endpoint": endpoint_2,
                            "protocol": "email",
                        },
                        notification_id_3: {
                            "endpoint": endpoint_3,
                            "protocol": "email",
                        },
                    },
                    "alertConfigs": {},
                },
            },
            "version": 1,
        }

    @pytest.fixture
    def user_config_provider(self, user_config):
        with patch("src.event.api.notification.v1.list.UserConfigProvider") as user_config_provider_mock:
            user_config_provider_mock.return_value.get_v2_user_config.return_value = user_config

            yield user_config_provider_mock

    def test_enact(self, make_event, user_id_1, user_config_provider, notification_id_1, endpoint_1):
        under_test = ListNotifications(make_event(user_id_1))

        result = under_test.enact()

        assert len(result) == 1
        assert result[0] == {
            "notificationId": notification_id_1,
            "endpoint": endpoint_1,
            "protocol": "email",
        }

    def test_enact_multiple(
        self, make_event, user_id_2, user_config_provider, notification_id_2, notification_id_3, endpoint_2, endpoint_3
    ):
        under_test = ListNotifications(make_event(user_id_2))

        result = under_test.enact()

        assert len(result) == 2
        assert result[0] == {
            "notificationId": notification_id_2,
            "endpoint": endpoint_2,
            "protocol": "email",
        }
        assert result[1] == {
            "notificationId": notification_id_3,
            "endpoint": endpoint_3,
            "protocol": "email",
        }

    def test_enact_unknown_user(self, make_event, user_config_provider):
        under_test = ListNotifications(make_event("someone"))

        result = under_test.enact()

        assert len(result) == 0

    def test_enact_no_object(self, make_event, user_config_provider):
        user_config_provider.return_value.get_v2_user_config.return_value = None

        under_test = ListNotifications(make_event("someone"))

        result = under_test.enact()

        assert len(result) == 0

    def test_enact_empty_object(self, make_event, user_config_provider):
        user_config_provider.return_value.get_v2_user_config.return_value = {}

        under_test = ListNotifications(make_event("someone"))

        result = under_test.enact()

        assert len(result) == 0

    def test_enact_missing_key(self, make_event, user_config_provider):
        user_config_provider.return_value.get_v2_user_config.return_value = {"asdf": "1234"}

        under_test = ListNotifications(make_event("someone"))

        result = under_test.enact()

        assert len(result) == 0
