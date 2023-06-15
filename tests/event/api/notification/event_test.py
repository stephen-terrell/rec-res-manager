import pytest
from unittest.mock import patch

from src.event.api.notification.event import NotificationEvent


class TestNotificationEvent:
    @pytest.fixture
    def handler_result(self):
        return {"asdf": "list alerts"}

    @pytest.fixture
    def list_notifications_mock(self, handler_result):
        with patch("src.event.api.notification.event.ListNotifications") as list_notifications_mock:
            list_notifications_mock.return_value.enact.return_value = handler_result

            yield list_notifications_mock

    def test_list(self, handler_result, list_notifications_mock):
        event = {"routeKey": "GET /notifications"}

        under_test = NotificationEvent(event, {})

        result = under_test.handle()

        list_notifications_mock.assert_called_once_with(event)

        assert result == handler_result

    @pytest.fixture
    def put_notification_mock(self, handler_result):
        with patch("src.event.api.notification.event.PutNotification") as put_notification_mock:
            put_notification_mock.return_value.enact.return_value = handler_result

            yield put_notification_mock

    def test_put(self, handler_result, put_notification_mock):
        event = {"routeKey": "PUT /notifications"}

        under_test = NotificationEvent(event, {})

        result = under_test.handle()

        put_notification_mock.assert_called_once_with(event)

        assert result == handler_result

    @pytest.fixture
    def delete_notification_mock(self, handler_result):
        with patch("src.event.api.notification.event.DeleteNotification") as delete_notification_mock:
            delete_notification_mock.return_value.enact.return_value = handler_result

            yield delete_notification_mock

    def test_delete(self, handler_result, delete_notification_mock):
        event = {"routeKey": "DELETE /notifications/{notificationId}"}

        under_test = NotificationEvent(event, {})

        result = under_test.handle()

        delete_notification_mock.assert_called_once_with(event)

        assert result == handler_result

    def test_invalid_route_key(self):
        event = {"routeKey": "invalid"}

        under_test = NotificationEvent(event, {})

        with pytest.raises(ValueError):
            under_test.handle()

    def test_missing_route_key(self):
        event = {"some": "other key"}

        under_test = NotificationEvent(event, {})

        with pytest.raises(ValueError):
            under_test.handle()
