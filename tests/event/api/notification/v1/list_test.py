import pytest
from unittest.mock import patch

from src.event.api.notification.v1.list import ListNotifications


class TestList:
    @pytest.fixture
    def user_id_1(self):
        return "stephen"

    @pytest.fixture
    def make_event(self):
        def _make_event(user_id):
            return {"headers": {"x-rec-res-user-id": user_id}}

        return _make_event

    @pytest.fixture
    def notification_id_1(self):
        return "id-1"

    @pytest.fixture
    def subscription_arn_1(self, notification_id_1):
        return "something:" + notification_id_1

    @pytest.fixture
    def endpoint_1(self):
        return "111111111"

    @pytest.fixture
    def list_subscriptions_mock(self, subscription_arn_1, endpoint_1):
        with patch("src.event.api.notification.v1.list.SnsProxy") as sns_proxy:
            sns_proxy.return_value.list_subscriptions.return_value = [
                {"SubscriptionArn": subscription_arn_1, "Protocol": "email", "Endpoint": endpoint_1}
            ]
            yield sns_proxy.return_value.list_subscriptions

    def test_enact(self, make_event, user_id_1, notification_id_1, endpoint_1, list_subscriptions_mock):
        under_test = ListNotifications(make_event(user_id_1))

        result = under_test.enact()

        assert len(result) == 1
        assert result[0] == {
            "notificationId": notification_id_1,
            "endpoint": endpoint_1,
            "protocol": "email",
        }

        list_subscriptions_mock.assert_called_once_with(user_id_1)

    def test_enact_pending_confirmation(
        self, make_event, user_id_1, notification_id_1, endpoint_1, list_subscriptions_mock
    ):
        list_subscriptions_mock.return_value.append(
            {"SubscriptionArn": "PendingConfirmation", "Protocol": "email", "Endpoint": "other.com"}
        )
        under_test = ListNotifications(make_event(user_id_1))

        result = under_test.enact()

        assert len(result) == 1
        assert result[0] == {
            "notificationId": notification_id_1,
            "endpoint": endpoint_1,
            "protocol": "email",
        }

        list_subscriptions_mock.assert_called_once_with(user_id_1)
