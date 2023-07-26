import pytest
from unittest.mock import patch

from src.event.api.notification.v1.delete import DeleteNotification


class TestDelete:
    @pytest.fixture
    def user_id_1(self):
        return "user1111111"

    @pytest.fixture
    def subscription_id_1(self):
        return "notificiation121212"

    @pytest.fixture
    def make_event(self):
        def _make_event(user_id, notification_id_1):
            return {"headers": {"x-rec-res-user-id": user_id}, "pathParameters": {"notificationId": notification_id_1}}

        return _make_event

    @pytest.fixture
    def remove_subscription_mock(self):
        with patch("src.event.api.notification.v1.delete.SnsProxy") as sns_proxy:
            yield sns_proxy.return_value.remove_subscription

    def test_enact(self, user_id_1, subscription_id_1, make_event, remove_subscription_mock):
        under_test = DeleteNotification(make_event(user_id_1, subscription_id_1))

        result = under_test.enact()

        assert result is None
        remove_subscription_mock.assert_called_once_with(user_id_1, subscription_id_1)
