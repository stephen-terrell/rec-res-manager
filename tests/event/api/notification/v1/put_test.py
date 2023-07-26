import pytest
from unittest.mock import patch

from src.event.api.notification.v1.put import PutNotification
from src.model.enum.protocol_type import ProtocolType
from src.model.subscription_config import SubscriptionConfig


class TestPut:
    @pytest.fixture
    def subscription_id_1(self):
        return "subscribe"

    @pytest.fixture
    def user_id_1(self):
        return "user1111111"

    @pytest.fixture
    def endpoint(self):
        return "test@test.com"

    @pytest.fixture
    def make_event(self):
        def _make_event(user_id, endpoint):
            return {
                "headers": {"x-rec-res-user-id": user_id},
                "body": {
                    "protocol": "email",
                    "endpoint": endpoint,
                },
            }

        return _make_event

    @pytest.fixture
    def sns_proxy_mock(self):
        with patch("src.event.api.notification.v1.put.SnsProxy") as sns_proxy:
            yield sns_proxy.return_value

    @pytest.fixture
    def create_subscription_mock(self, sns_proxy_mock):
        return sns_proxy_mock.create_subscription

    @pytest.fixture
    def topic_exists_mock(self, sns_proxy_mock):
        sns_proxy_mock.topic_exists.return_value = True
        return sns_proxy_mock.topic_exists

    @pytest.fixture
    def create_topic_mock(self, sns_proxy_mock):
        return sns_proxy_mock.create_topic

    def test_enact(
        self, user_id_1, subscription_id_1, endpoint, make_event, create_subscription_mock, create_topic_mock
    ):
        create_subscription_mock.return_value = subscription_id_1
        under_test = PutNotification(make_event(user_id_1, endpoint))

        result = under_test.enact()

        data = {"userId": user_id_1, "notificationId": subscription_id_1, "protocol": "email", "endpoint": endpoint}

        assert result == data
        create_subscription_mock.assert_called_once_with(user_id_1, SubscriptionConfig(endpoint, ProtocolType.EMAIL))
        create_topic_mock.assert_not_called()

    def test_enact_missing_user(
        self,
        user_id_1,
        subscription_id_1,
        endpoint,
        make_event,
        create_subscription_mock,
        create_topic_mock,
        topic_exists_mock,
    ):
        topic_exists_mock.return_value = False
        create_subscription_mock.return_value = subscription_id_1
        under_test = PutNotification(make_event(user_id_1, endpoint))

        result = under_test.enact()

        data = {"userId": user_id_1, "notificationId": subscription_id_1, "protocol": "email", "endpoint": endpoint}

        assert result == data
        create_subscription_mock.assert_called_once_with(user_id_1, SubscriptionConfig(endpoint, ProtocolType.EMAIL))
        create_topic_mock.assert_called_once_with(user_id_1)
